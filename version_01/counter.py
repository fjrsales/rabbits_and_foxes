
# counter.py
class Counter:
    """
    Fornece um contador para um participante na simulação.
    Inclui uma string identificadora e um contador de quantos
    participantes deste tipo existem atualmente na simulação.
    """

    def __init__(self, name):
        """
        Fornece um nome para um dos tipos de simulação.
        :param name: Um nome, ex: "Fox"
        """
        self.name = name
        self.count = 0

    def get_name(self):
        """Retorna a descrição curta deste tipo."""
        return self.name

    def get_count(self):
        """Retorna o contador atual para este tipo."""
        return self.count

    def increment(self):
        """Incrementa o contador atual em um."""
        self.count += 1

    def reset(self):
        """Redefine o contador atual para zero."""
        self.count = 0
