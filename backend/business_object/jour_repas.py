class JourRepas:
    """
    Représente les repas d'une journée dans un planning de repas.
    """

    MOMENTS = ["petit_dejeuner", "dejeuner", "diner"]

    def __init__(self, numero_jour: int):
        self.numero_jour = numero_jour
        self._repas = dict.fromkeys(self.MOMENTS)

    def ajouter_plat(self, moment: str, id_plat: int):
        if moment not in self.MOMENTS:
            raise ValueError("Moment invalide")
        self._repas[moment] = id_plat

    def get_plat(self, moment: str):
        return self._repas.get(moment)

    def to_dict(self):
        return self._repas.copy()

    def __str__(self):
        return f"JourRepas({self.numero_jour}, {self._repas})"
