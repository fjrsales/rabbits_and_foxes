# field.py
from randomizer import Randomizer
from rabbit import Rabbit
from fox import Fox
from location import Location

class Field:
    """
    Representa uma grade retangular de posições de campo.
    Cada posição é capaz de armazenar um único animal/objeto.
    """

    def __init__(self, depth, width):
        """
        Representa um campo com as dimensões dadas.
        """
        self.depth = depth
        self.width = width
        self.field = {}  # Animais mapeados por localização
        self.rabbits = []  # Os dois tipos de animal
        self.foxes = []
        self._rand = Randomizer.get_random()

    def place_rabbit(self, rabbit, location):
        """
        Coloca um coelho na localização dada.
        Se já houver um animal na localização, ele será perdido.
        """
        assert location is not None
        other = self.field.get(location)

        if isinstance(other, Rabbit):
            self.rabbits.remove(other)
        elif isinstance(other, Fox):
            self.foxes.remove(other)

        self.field[location] = rabbit
        self.rabbits.append(rabbit)

    def place_fox(self, fox, location):
        """
        Coloca uma raposa na localização dada.
        Se já houver um animal na localização, ele será perdido.
        """
        assert location is not None
        other = self.field.get(location)

        if isinstance(other, Rabbit):
            self.rabbits.remove(other)
        elif isinstance(other, Fox):
            self.foxes.remove(other)

        self.field[location] = fox
        self.foxes.append(fox)


    def get_object_at(self, location):
        """
        Retorna o animal na localização dada, se houver.
        """
        return self.field.get(location)

    def get_free_adjacent_locations(self, location):
        """
        Obtém uma lista embaralhada das localizações adjacentes livres.
        """
        free = []
        adjacent = self.get_adjacent_locations(location)

        for next_location in adjacent:
            animal = self.field.get(next_location)
            if animal is None:
                free.append(next_location)
            else:
                if isinstance(animal, Rabbit) and not animal.is_alive():
                    free.append(next_location)
                elif isinstance(animal, Fox) and not animal.is_alive():
                    free.append(next_location)


        return free


    def get_adjacent_locations(self, location):
        """
        Retorna uma lista embaralhada de localizações adjacentes à dada.
        A lista não incluirá a própria localização.
        Todas as localizações estarão dentro da grade.
        """
        locations = []
        if location is not None:
            row = location.row
            col = location.col

            for roffset in range(-1, 2):
                next_row = row + roffset
                if 0 <= next_row < self.depth:
                    for coffset in range(-1, 2):
                        next_col = col + coffset
                        # Exclui localizações inválidas e a localização original
                        if (0 <= next_col < self.width and
                            (roffset != 0 or coffset != 0)):
                            locations.append(Location(next_row, next_col))

            # Embaralha a lista. Vários outros métodos dependem da lista
            # estar em ordem aleatória
            self._rand.shuffle(locations) # Corrected line

        return locations

    def field_stats(self):
        """Imprime o número de raposas e coelhos no campo."""
        num_foxes = 0
        num_rabbits = 0

        for animal in self.field.values():
            if isinstance(animal, Fox) and animal.is_alive():
                num_foxes += 1
            elif isinstance(animal, Rabbit) and animal.is_alive():
                num_rabbits += 1

        print(f"Rabbits: {num_rabbits} Foxes: {num_foxes}")


    def clear(self):
        """Esvazia o campo."""
        self.field.clear()
        self.rabbits.clear()
        self.foxes.clear()

    def is_viable(self):
        """
        Retorna se há pelo menos um coelho e uma raposa no campo.
        """
        has_rabbits = any(rabbit.is_alive() for rabbit in self.rabbits)
        has_foxes = any(fox.is_alive() for fox in self.foxes)
        return has_rabbits and has_foxes

    def get_depth(self):
        """Retorna a profundidade do campo."""
        return self.depth

    def get_width(self):
        """Retorna a largura do campo."""
        return self.width

    def get_rabbits(self):
        """Retorna uma lista dos coelhos que estão vivos."""
        return [rabbit for rabbit in self.rabbits if rabbit.is_alive()]

    def get_foxes(self):
        """Retorna uma lista das raposas que estão vivas."""
        return [fox for fox in self.foxes if fox.is_alive()]
