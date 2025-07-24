from randomizer import Randomizer
from location import Location

# rabbit.py
class Rabbit:
    """
    Um modelo simples de um coelho.
    Coelhos envelhecem, se movem, procriam e morrem.
    """

    # Características compartilhadas por todos os coelhos (variáveis de classe)
    BREEDING_AGE = 5  # A idade na qual um coelho pode começar a procriar
    MAX_AGE = 40      # A idade até a qual um coelho pode viver
    BREEDING_PROBABILITY = 0.12  # A probabilidade de um coelho procriar
    MAX_LITTER_SIZE = 4          # O número máximo de nascimentos

    def __init__(self, random_age, location):
        """
        Cria um novo coelho. Um coelho pode ser criado com idade
        zero (recém-nascido) ou com idade aleatória.
        """
        self.age = 0
        self.alive = True
        self.location = location

        rand = Randomizer.get_random()
        if random_age:
            self.age = rand.randint(0, self.MAX_AGE - 1)

    def run(self, current_field, next_field_state):
        """
        Isto é o que o coelho faz na maior parte do tempo - ele corre
        por aí. Às vezes ele procria ou morre de idade.
        """
        self._increment_age()
        if self.alive:
            free_locations = next_field_state.get_free_adjacent_locations(self.location)
            if free_locations:
                self._give_birth(next_field_state, free_locations)

            # Tenta se mover para uma localização livre
            if free_locations:
                new_location = free_locations[0]
                self.location = new_location
                next_field_state.place_rabbit(self, new_location)
            else:
                # Superpopulação
                self.set_dead()

    def is_alive(self):
        """Verifica se o coelho está vivo ou não."""
        return self.alive

    def set_dead(self):
        """
        Indica que o coelho não está mais vivo.
        Ele é removido do campo.
        """
        self.alive = False
        self.location = None

    def get_location(self):
        """Retorna a localização do coelho."""
        return self.location

    def __str__(self):
        return f"Rabbit(age={self.age}, alive={self.alive}, location={self.location})"

    def _increment_age(self):
        """
        Aumenta a idade.
        Isto pode resultar na morte do coelho.
        """
        self.age += 1
        if self.age > self.MAX_AGE:
            self.set_dead()

    def _give_birth(self, next_field_state, free_locations):
        """
        Verifica se este coelho deve dar à luz neste passo.
        Novos nascimentos serão feitos em localizações adjacentes livres.
        """
        births = self._breed()
        if births > 0:
            for b in range(births):
                if not free_locations:
                    break
                loc = free_locations.pop(0)
                young = Rabbit(False, loc)
                next_field_state.place_rabbit(young, loc)

    def _breed(self):
        """
        Gera um número representando o número de nascimentos,
        se pode procriar.
        """
        rand = Randomizer.get_random()
        if self._can_breed() and rand.random() <= self.BREEDING_PROBABILITY:
            return rand.randint(1, self.MAX_LITTER_SIZE)
        else:
            return 0

    def _can_breed(self):
        """Um coelho pode procriar se atingiu a idade de procriação."""
        return self.age >= self.BREEDING_AGE
