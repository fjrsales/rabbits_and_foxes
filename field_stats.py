
# field_stats.py
from counter import Counter
from location import Location

class FieldStats:
    """
    Esta classe coleta e fornece alguns dados estatísticos sobre o estado
    de um campo. É flexível: criará e manterá um contador para qualquer
    classe de objeto encontrada no campo.
    """

    def __init__(self):
        """Constrói um objeto FieldStats."""
        # Contadores para cada tipo de entidade (raposa, coelho, etc.) na simulação
        self.counters = {}
        # Se os contadores estão atualmente atualizados
        self.counts_valid = True


    def get_population_details(self, field):
        """
        Obtém detalhes do que está no campo.
        :return: Uma string descrevendo o que está no campo
        """
        if not self.counts_valid:
            self._generate_counts(field)

        details = []
        for class_type, counter in self.counters.items():
            details.append(f"{counter.get_name()}: {counter.get_count()}")

        return " ".join(details)


    def reset(self):
        """
        Invalida o conjunto atual de estatísticas; redefine todos
        os contadores para zero.
        """
        self.counts_valid = False
        for counter in self.counters.values():
            counter.reset()


    def increment_count(self, animal_class):
        """
        Incrementa o contador para uma classe de animal.
        :param animal_class: A classe do animal a incrementar
        """
        if animal_class not in self.counters:
            # Ainda não temos um contador para esta espécie.
            # Cria um.
            self.counters[animal_class] = Counter(animal_class.__name__)

        self.counters[animal_class].increment()


    def count_finished(self):
        """Indica que uma contagem de animais foi completada."""
        self.counts_valid = True


    def is_viable(self, field):
        """
        Determina se a simulação ainda é viável.
        Ou seja, se deve continuar a executar.
        :return: true se há mais de uma espécie viva
        """
        return self.stats.is_viable(field)


    def _generate_counts(self, field):
        """
        Generates counts of the number of foxes and rabbits.
        These are not kept up to date as foxes and rabbits
        are placed on the field, but only when a request
        is made for the information.
        """
        self.reset()
        for row in range(field.get_depth()):
            for col in range(field.get_width()):
                animal = field.get_object_at(Location(row, col))
                if animal is not None:
                    self.increment_count(type(animal))
        self.counts_valid = True
