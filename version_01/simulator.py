from field import Field
from simulator_view import SimulatorView
from randomizer import Randomizer
from rabbit import Rabbit
from fox import Fox
from location import Location
import time

# simulator.py
class Simulator:
    """
    Um simulador simples predador-presa, baseado em um campo retangular
    contendo coelhos e raposas.
    """

    # Constantes representando informações de configuração para a simulação
    DEFAULT_WIDTH = 120   # A largura padrão da grade
    DEFAULT_DEPTH = 80    # A profundidade padrão da grade
    FOX_CREATION_PROBABILITY = 0.2      # A probabilidade de uma raposa ser criada
    RABBIT_CREATION_PROBABILITY = 0.08   # A probabilidade de um coelho ser criado

    def __init__(self, depth=None, width=None):
        """
        Cria um campo de simulação com o tamanho dado.
        """
        if depth is None:
            depth = self.DEFAULT_DEPTH
        if width is None:
            width = self.DEFAULT_WIDTH

        if width <= 0 or depth <= 0:
            print("As dimensões devem ser >= zero.")
            print("Usando valores padrão.")
            depth = self.DEFAULT_DEPTH
            width = self.DEFAULT_WIDTH

        self.field = Field(depth, width)
        self.view = SimulatorView(depth, width)
        self.step = 0

        self.reset()

    def run_long_simulation(self):
        """
        Executa a simulação a partir de seu estado atual por um
        período razoavelmente longo (4000 passos).
        """
        self.simulate(4000)

    def simulate(self, num_steps):
        """
        Executa a simulação pelo número dado de passos.
        Para antes do número dado de passos se deixar de ser viável.
        """
        self.report_stats()
        for n in range(1, num_steps + 1):
            if not self.field.is_viable():
                break
            self.simulate_one_step()
            self._delay(100)  # ajuste isto para mudar a velocidade de execução

    def simulate_one_step(self):
        """
        Executa a simulação a partir de seu estado atual por um único passo.
        Itera sobre todo o campo atualizando o estado de cada raposa e coelho.
        """
        self.step += 1
        # Usa um Field separado para armazenar o estado inicial do próximo passo
        next_field_state = Field(self.field.get_depth(), self.field.get_width())

        rabbits = self.field.get_rabbits()
        foxes = self.field.get_foxes()

        # Deixa todos os coelhos correrem
        for rabbit in rabbits:
            rabbit.run(self.field, next_field_state)

        # Deixa todas as raposas caçarem
        for fox in foxes:
            fox.hunt(self.field, next_field_state)

        # Substitui o estado antigo pelo novo
        self.field = next_field_state

        self.report_stats()
        self.view.show_status(self.step, self.field)

    def reset(self):
        """Redefine a simulação para uma posição inicial."""
        self.step = 0
        self._populate()
        self.view.show_status(self.step, self.field)

    def report_stats(self):
        """Relata o número de cada tipo de animal no campo."""
        print(f"Step: {self.step} ", end="")
        self.field.field_stats()

    def _populate(self):
        """Popula aleatoriamente o campo com raposas e coelhos."""
        rand = Randomizer.get_random()
        self.field.clear()

        for row in range(self.field.get_depth()):
            for col in range(self.field.get_width()):
                if rand.random() <= self.FOX_CREATION_PROBABILITY:
                    location = Location(row, col)
                    fox = Fox(True, location)
                    self.field.place_fox(fox, location)
                elif rand.random() <= self.RABBIT_CREATION_PROBABILITY:
                    location = Location(row, col)
                    rabbit = Rabbit(True, location)
                    self.field.place_rabbit(rabbit, location)
                # senão deixa a localização vazia

    def _delay(self, milliseconds):
        """
        Pausa por um tempo dado.
        :param milliseconds: O tempo para pausar, em milissegundos
        """
        time.sleep(milliseconds / 1000.0)


# main.py - exemplo de uso
if __name__ == "__main__":
    print("=== Simulação Foxes and Rabbits ===")
    print("Comandos disponíveis:")
    print("1 - Simular um passo")
    print("2 - Simular N passos")
    print("3 - Executar simulação longa (4000 passos)")
    print("4 - Resetar simulação")
    print("0 - Sair")

    # Cria o simulador
    simulator = Simulator(40, 60)  # Campo menor para melhor visualização

    while True:
        try:
            choice = input("\nEscolha uma opção: ").strip()
            if choice == "0":
                print("Encerrando simulação...")
                break
            elif choice == "1":
                simulator.simulate_one_step()
            elif choice == "2":
                try:
                    steps = int(input("Número de passos: "))
                    if steps > 0:
                        simulator.simulate(steps)
                    else:
                        print("Número de passos deve ser positivo.")
                except ValueError:
                    print("Por favor, digite um número válido.")
            elif choice == "3":
                print("Iniciando simulação longa...")
                simulator.run_long_simulation()
            elif choice == "4":
                simulator.reset()
                print("Simulação resetada.")
            else:
                print("Opção inválida. Tente novamente.")

        except KeyboardInterrupt:
            print("\n\nSimulação interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"Erro: {e}")

    print("Simulação finalizada.")
