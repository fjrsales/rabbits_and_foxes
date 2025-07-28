# fox.py
from randomizer import Randomizer
from rabbit import Rabbit

class Fox:
    """
    Um modelo simples de uma raposa.
    Raposas envelhecem, se movem, comem coelhos e morrem.
    """

    # Características compartilhadas por todas as raposas (variáveis de classe)
    BREEDING_AGE = 15        # A idade na qual uma raposa pode começar a procriar
    MAX_AGE = 150           # A idade até a qual uma raposa pode viver
    BREEDING_PROBABILITY = 0.08  # A probabilidade de uma raposa procriar
    MAX_LITTER_SIZE = 2     # O número máximo de nascimentos
    RABBIT_FOOD_VALUE = 9   # O valor alimentar de um único coelho

    def __init__(self, random_age, location):
        """
        Cria uma raposa. Uma raposa pode ser criada como recém-nascida
        (idade zero e sem fome) ou com idade e nível de fome aleatórios.
        """
        self.alive = True
        self.location = location
        self.age = 0

        rand = Randomizer.get_random()
        if random_age:
            self.age = rand.randint(0, self.MAX_AGE - 1)

        self.food_level = rand.randint(0, self.RABBIT_FOOD_VALUE - 1)

    def hunt(self, current_field, next_field_state):
        """
        Isto é o que a raposa faz na maior parte do tempo: ela caça
        coelhos. No processo, ela pode procriar, morrer de fome ou
        morrer de idade.
        """
        self._increment_age()
        self._increment_hunger()

        if self.alive:
            free_locations = next_field_state.get_free_adjacent_locations(self.location)
            if free_locations:
                self._give_birth(next_field_state, free_locations)

            # Move em direção a uma fonte de comida se encontrada
            new_location = self._find_food(current_field)
            if new_location is None and free_locations:
                # Nenhuma comida encontrada - tenta se mover para uma localização livre
                new_location = free_locations.pop(0)

            # Verifica se foi possível se mover
            if new_location is not None:
                self.location = new_location
                next_field_state.place_fox(self, new_location)
            else:
                # Superpopulação
                self.set_dead()

    def is_alive(self):
        """Verifica se a raposa está viva ou não."""
        return self.alive

    def get_location(self):
        """Retorna a localização da raposa."""
        return self.location

    def set_dead(self):
        """
        Indica que a raposa não está mais viva.
        Ela é removida do campo.
        """
        self.alive = False
        self.location = None

    def __str__(self):
        return f"Fox(age={self.age}, alive={self.alive}, location={self.location}, food_level={self.food_level})"

    def _increment_age(self):
        """Aumenta a idade. Isto pode resultar na morte da raposa."""
        self.age += 1
        if self.age > self.MAX_AGE:
            self.set_dead()

    def _increment_hunger(self):
        """Deixa esta raposa com mais fome. Isto pode resultar na morte da raposa."""
        self.food_level -= 1
        if self.food_level <= 0:
            self.set_dead()

    def _find_food(self, field):
        """
        Procura por coelhos adjacentes à localização atual.
        Apenas o primeiro coelho vivo é comido.
        """
        adjacent = field.get_adjacent_locations(self.location)

        for loc in adjacent:
            animal = field.get_object_at(loc)
            if isinstance(animal, Rabbit) and animal.is_alive():
                animal.set_dead()
                self.food_level = self.RABBIT_FOOD_VALUE
                return loc

        return None

    def _give_birth(self, next_field_state, free_locations):
        """
        Verifica se esta raposa deve dar à luz neste passo.
        Novos nascimentos serão feitos em localizações adjacentes livres.
        """
        births = self._breed()
        if births > 0:
            for b in range(births):
                if not free_locations:
                    break
                loc = free_locations.pop(0)
                young = Fox(False, loc)
                next_field_state.place_fox(young, loc)

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
        """Uma raposa pode procriar se atingiu a idade de procriação."""
        return self.age >= self.BREEDING_AGE
