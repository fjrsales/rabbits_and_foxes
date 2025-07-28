# randomizer.py
import random

class Randomizer:
    """
    Fornece controle sobre a aleatoriedade da simulação. Usando o
    randomizador compartilhado com semente fixa, execuções repetidas
    terão exatamente o mesmo comportamento (útil para testes).
    """

    # A semente padrão para controle da aleatoriedade
    SEED = 1111
    # Um objeto Random compartilhado, se necessário
    _rand = random.Random(SEED)
    # Determina se um gerador aleatório compartilhado deve ser fornecido
    USE_SHARED = True

    @staticmethod
    def get_random():
        """Fornece um gerador aleatório."""
        if Randomizer.USE_SHARED:
            return Randomizer._rand
        else:
            return random.Random()

    @staticmethod
    def reset():
        """
        Redefine a aleatoriedade.
        Não terá efeito se a aleatoriedade não for através de um
        gerador Random compartilhado.
        """
        if Randomizer.USE_SHARED:
            Randomizer._rand.seed(Randomizer.SEED)
