class JourRepas:
    """
    Classe représentant les repas d'une journée.
    Comprend un plat pour chaque moment de la journée : petit-déjeuner, déjeuner, dîner.
    """

    def __init__(self, petit_dejeuner=None, dejeuner=None, diner=None):
        self.petit_dejeuner = petit_dejeuner
        self.dejeuner = dejeuner
        self.diner = diner

    def __str__(self):
        return f"JourRepas(petit_dejeuner={self.petit_dejeuner}, dejeuner={self.dejeuner}, diner={self.diner})"
