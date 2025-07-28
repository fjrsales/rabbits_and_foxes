# location.py
class Location:
    """Representa uma localização em uma grade retangular."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self):
        return hash((self.row, self.col))

    def __str__(self):
        return f"Location({self.row}, {self.col})"

    def __repr__(self):
        return self.__str__()
