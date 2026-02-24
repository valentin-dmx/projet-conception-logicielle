class PlanningRepas:
    """
    Classe représentant un plan de repas.
    Comprend une série de plats pour chaque moment de la journée (petit-déjeuner, déjeuner, dîner), sur une série de plusieurs jours.
    """

    def __init__(self, nb_jours):
        self.nb_jours = nb_jours
        for i in range(1, nb_jours + 1):
            setattr(
                self,
                f"jour_{i}",
                {"petit_dejeuner": None, "dejeuner": None, "diner": None},
            )

    def __str__(self):
        return f"PlanningRepas(nb_jours={self.nb_jours}, jours={[getattr(self, f'jour_{i}') for i in range(1, self.nb_jours + 1)]})"
