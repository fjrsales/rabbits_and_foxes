#simulator_view.py
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os
from field_stats import FieldStats
from location import Location
from IPython.display import display, HTML, Image


class SimulatorView:
    """
    Uma visualização gráfica da grade de simulação para Google Colab.
    Não interfere com o input do usuário.
    """

    def __init__(self, height, width):
        """
        Cria uma visualização com a altura e largura dadas.
        """
        self.height = height
        self.width = width
        self.stats = FieldStats()

        # Define cores para cada tipo de animal
        self.colors = {
            'Rabbit': 1,  # Verde
            'Fox': 2,     # Vermelho
            'Empty': 0    # Branco/Transparente
        }

        # Configuração do matplotlib
        self.colormap = ListedColormap(['white', 'lightgreen', 'red'])

        # Histórico de populações para gráficos
        self.population_history = {
            'steps': [],
            'rabbits': [],
            'foxes': [],
            'total': []
        }

        # Controla frequência de atualização
        self.update_frequency = 25  # Atualiza gráfico a cada 25 steps
        self.print_frequency = 50   # Imprime info a cada 50 steps

        # Configuração do matplotlib para não interferir com input
        plt.ioff()  # Desativa modo interativo

        # Cria diretório para salvar imagens
        self.image_dir = "simulation_images"
        self.setup_image_directory()

        # Cria área de visualização dedicada
        self.setup_display_area()

    def setup_image_directory(self):
        """Cria diretório para salvar as imagens da simulação."""
        try:
            if not os.path.exists(self.image_dir):
                os.makedirs(self.image_dir)
                print(f"📁 Diretório criado: {self.image_dir}")
            else:
                print(f"📁 Usando diretório existente: {self.image_dir}")
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível criar diretório {self.image_dir}: {e}")
            # Fallback para diretório atual
            self.image_dir = "."

    def setup_display_area(self):
        """Configura área dedicada para visualização."""
        try:
            display(HTML("""
            <div id="simulation-display" style="margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                <h3>🐰🦊 Simulação Predador-Presa</h3>
                <p>A visualização aparecerá aqui durante a simulação...</p>
            </div>
            """))
        except Exception as e:
            print(f"📱 Modo terminal detectado - visualização adaptada")

    def set_color(self, animal_class, symbol):
        """
        Define um símbolo/cor a ser usado para uma dada classe de animal.
        """
        if hasattr(animal_class, '__name__'):
            class_name = animal_class.__name__
        else:
            class_name = str(animal_class)

        # Mapeia símbolos para códigos de cor
        symbol_to_color = {
            'R': 1,  # Rabbit -> Verde
            'F': 2,  # Fox -> Vermelho
        }

        if symbol in symbol_to_color:
            self.colors[class_name] = symbol_to_color[symbol]

    def show_status(self, step, field):
        """
        Mostra o status atual do campo.
        """
        # Sempre atualiza as estatísticas
        self.stats.reset()

        # Conta populações
        rabbit_count = 0
        fox_count = 0

        for row in range(field.get_depth()):
            for col in range(field.get_width()):
                animal = field.get_object_at(Location(row, col))
                if animal is not None:
                    self.stats.increment_count(type(animal))
                    animal_type = type(animal).__name__

                    if animal_type == 'Rabbit':
                        rabbit_count += 1
                    elif animal_type == 'Fox':
                        fox_count += 1

        self.stats.count_finished()

        # Sempre adiciona ao histórico
        self.population_history['steps'].append(step)
        self.population_history['rabbits'].append(rabbit_count)
        self.population_history['foxes'].append(fox_count)
        self.population_history['total'].append(rabbit_count + fox_count)

        # Imprime informações de forma compacta
        if step % self.print_frequency == 0:
            print(f"Step {step:4d} | 🐰 {rabbit_count:4d} | 🦊 {fox_count:3d} | Total: {rabbit_count + fox_count:4d}")

        # Atualiza gráficos periodicamente
        if step % self.update_frequency == 0:
            self.create_and_save_plots(field, step, rabbit_count, fox_count)

    def create_and_save_plots(self, field, step, rabbit_count, fox_count):
        """Cria e salva gráficos da simulação."""

        try:
            # Cria figura
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            fig.patch.set_facecolor('white')
            fig.suptitle(f"Simulação Predador-Presa - Step {step}", fontsize=16, fontweight='bold')

            # Plot 1: Grade do campo (amostra)
            grid_matrix = np.zeros((field.get_depth(), field.get_width()))

            for row in range(field.get_depth()):
                for col in range(field.get_width()):
                    animal = field.get_object_at(Location(row, col))
                    if animal is not None:
                        animal_type = type(animal).__name__
                        if animal_type == 'Rabbit':
                            grid_matrix[row][col] = 1
                        elif animal_type == 'Fox':
                            grid_matrix[row][col] = 2

            # Mostra amostra do campo (limitado para visualização)
            max_rows = min(40, field.get_depth())
            max_cols = min(60, field.get_width())
            display_grid = grid_matrix[:max_rows, :max_cols]

            im = axes[0].imshow(display_grid, cmap=self.colormap, vmin=0, vmax=2, aspect='equal')
            axes[0].set_title(f"Campo - Step {step}\n Coelhos: {rabbit_count} |  Raposas: {fox_count}")
            axes[0].set_xlabel(f"Largura (mostrando {max_cols}/{field.get_width()})")
            axes[0].set_ylabel(f"Altura (mostrando {max_rows}/{field.get_depth()})")

            # Adiciona legenda de cores
            legend_elements = [
                plt.Rectangle((0,0),1,1, facecolor='lightgreen', label='Coelhos'),
                plt.Rectangle((0,0),1,1, facecolor='red', label='Raposas'),
                plt.Rectangle((0,0),1,1, facecolor='white', edgecolor='black', label='Vazio')
            ]
            axes[0].legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))

            # Adiciona info se o campo foi truncado
            if field.get_depth() > max_rows or field.get_width() > max_cols:
                axes[0].text(0.02, 0.02, f"Amostra: {max_rows}×{max_cols}\nCampo real: {field.get_depth()}×{field.get_width()}",
                            transform=axes[0].transAxes,
                            verticalalignment='bottom',
                            fontsize=8,
                            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

            # Plot 2: Evolução populacional
            if len(self.population_history['steps']) > 1:
                axes[1].plot(self.population_history['steps'],
                           self.population_history['rabbits'],
                           'g-', label='Coelhos', linewidth=2.5, marker='o', markersize=3)
                axes[1].plot(self.population_history['steps'],
                           self.population_history['foxes'],
                           'r-', label='Raposas', linewidth=2.5, marker='s', markersize=3)

                # Destaca ponto atual com marcadores maiores
                axes[1].plot(step, rabbit_count, 'go', markersize=8, markeredgecolor='darkgreen', markeredgewidth=2)
                axes[1].plot(step, fox_count, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2)

                # Adiciona texto com valores atuais
                axes[1].text(0.02, 0.98, f"Atual:\n Coelhos {rabbit_count}\nRaposas {fox_count}",
                           transform=axes[1].transAxes,
                           verticalalignment='top',
                           fontsize=10,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))

            axes[1].set_title("Evolução Populacional")
            axes[1].set_xlabel("Steps")
            axes[1].set_ylabel("População")
            axes[1].legend(loc='upper right')
            axes[1].grid(True, alpha=0.3)

            # Define limites do eixo y para melhor visualização
            if len(self.population_history['steps']) > 1:
                max_pop = max(max(self.population_history['rabbits']), max(self.population_history['foxes']))
                axes[1].set_ylim(0, max_pop * 1.1)

            plt.tight_layout()

            # Salva a imagem
            filename = f"{self.image_dir}/simulation_step_{step:06d}.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')

            print(f"💾 Gráfico salvo: {filename}")

            # Exibe a imagem se estivermos no Colab/Jupyter
            try:
                display(Image(filename))
            except Exception:
                # Se não conseguir exibir, pelo menos confirma que salvou
                print(f"📊 Gráfico do Step {step} salvo com sucesso!")

            plt.close(fig)  # Fecha para liberar memória

        except Exception as e:
            print(f"❌ Erro ao criar/salvar gráfico do Step {step}: {e}")
            # Tenta criar pelo menos um gráfico simples
            self.create_simple_plot_fallback(step, rabbit_count, fox_count)

    def create_simple_plot_fallback(self, step, rabbit_count, fox_count):
        """Cria um gráfico simples como fallback em caso de erro."""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))

            if len(self.population_history['steps']) > 1:
                ax.plot(self.population_history['steps'],
                       self.population_history['rabbits'],
                       'g-', label='Coelhos', linewidth=2)
                ax.plot(self.population_history['steps'],
                       self.population_history['foxes'],
                       'r-', label='Raposas', linewidth=2)

            ax.set_title(f"População - Step {step}")
            ax.set_xlabel("Steps")
            ax.set_ylabel("População")
            ax.legend()
            ax.grid(True, alpha=0.3)

            filename = f"{self.image_dir}/simple_step_{step:06d}.png"
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            plt.close(fig)

            print(f"💾 Gráfico simples salvo: {filename}")

        except Exception as e:
            print(f"❌ Erro mesmo no gráfico simples: {e}")

    def is_viable(self, field):
        """
        Determina se a simulação deve continuar a executar.
        """
        return field.is_viable()

    def set_update_frequency(self, steps):
        """Define frequência de atualização dos gráficos."""
        self.update_frequency = max(1, steps)
        print(f"📊 Gráficos serão salvos a cada {self.update_frequency} steps")

    def set_print_frequency(self, steps):
        """Define frequência de informações no console."""
        self.print_frequency = max(1, steps)
        print(f"📝 Console atualizará a cada {self.print_frequency} steps")

    def show_final_results(self):
        """Mostra resultados finais da simulação."""

        if len(self.population_history['steps']) == 0:
            print("❌ Nenhum dado de simulação disponível.")
            return None

        final_step = self.population_history['steps'][-1]
        final_rabbits = self.population_history['rabbits'][-1]
        final_foxes = self.population_history['foxes'][-1]
        max_rabbits = max(self.population_history['rabbits'])
        max_foxes = max(self.population_history['foxes'])

        # Informações textuais
        print("\n" + "="*60)
        print("🏁 SIMULAÇÃO FINALIZADA")
        print("="*60)
        print(f"📊 Steps executados: {final_step}")
        print(f"🐰 Coelhos: {final_rabbits} (máximo: {max_rabbits})")
        print(f"🦊 Raposas: {final_foxes} (máximo: {max_foxes})")
        print(f"📈 População total final: {final_rabbits + final_foxes}")
        print(f"📁 Gráficos salvos em: {os.path.abspath(self.image_dir)}")
        print("="*60)

        # Cria gráfico final resumo
        self.create_final_summary_plot()

        return {
            'final_step': final_step,
            'final_rabbits': final_rabbits,
            'final_foxes': final_foxes,
            'max_rabbits': max_rabbits,
            'max_foxes': max_foxes,
            'history': self.population_history.copy(),
            'image_directory': os.path.abspath(self.image_dir)
        }

    def create_final_summary_plot(self):
        """Cria gráfico final resumo da simulação."""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 8))
            fig.patch.set_facecolor('white')

            if len(self.population_history['steps']) > 1:
                ax.plot(self.population_history['steps'],
                       self.population_history['rabbits'],
                       'g-', label='🐰 Coelhos', linewidth=3, alpha=0.8)
                ax.plot(self.population_history['steps'],
                       self.population_history['foxes'],
                       'r-', label='🦊 Raposas', linewidth=3, alpha=0.8)

                # Marca pontos de máximo
                max_rabbits = max(self.population_history['rabbits'])
                max_foxes = max(self.population_history['foxes'])
                max_r_step = self.population_history['steps'][self.population_history['rabbits'].index(max_rabbits)]
                max_f_step = self.population_history['steps'][self.population_history['foxes'].index(max_foxes)]

                ax.plot(max_r_step, max_rabbits, 'go', markersize=12,
                       label=f'Max Coelhos: {max_rabbits} (Step {max_r_step})')
                ax.plot(max_f_step, max_foxes, 'ro', markersize=12,
                       label=f'Max Raposas: {max_foxes} (Step {max_f_step})')

            ax.set_title("🐰🦊 Simulação Predador-Presa - Resultado Final",
                        fontsize=16, fontweight='bold')
            ax.set_xlabel("Steps", fontsize=12)
            ax.set_ylabel("População", fontsize=12)
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            plt.tight_layout()

            # Salva gráfico final
            final_filename = f"{self.image_dir}/FINAL_simulation_summary.png"
            plt.savefig(final_filename, dpi=300, bbox_inches='tight', facecolor='white')

            print(f"📊 Resumo final salvo: {final_filename}")

            # Tenta exibir
            try:
                display(Image(final_filename))
                plt.show()
            except:
                print("📱 Gráfico salvo - visualize o arquivo para ver o resultado final")

            plt.close(fig)

        except Exception as e:
            print(f"❌ Erro ao criar gráfico final: {e}")

    def list_saved_images(self):
        """Lista todas as imagens salvas da simulação."""
        try:
            files = [f for f in os.listdir(self.image_dir) if f.endswith('.png')]
            files.sort()

            print(f"\n📁 Imagens salvas em {os.path.abspath(self.image_dir)}:")
            for i, file in enumerate(files, 1):
                print(f"  {i:3d}. {file}")

            print(f"\n📊 Total: {len(files)} imagens")

        except Exception as e:
            print(f"❌ Erro ao listar imagens: {e}")

    def clean_saved_images(self):
        """Remove todas as imagens salvas da simulação."""
        try:
            files = [f for f in os.listdir(self.image_dir) if f.endswith('.png')]

            for file in files:
                os.remove(os.path.join(self.image_dir, file))

            print(f"🧹 Removidas {len(files)} imagens do diretório {self.image_dir}")

        except Exception as e:
            print(f"❌ Erro ao limpar imagens: {e}")
