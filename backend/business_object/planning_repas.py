from backend.business_object.jour_repas import JourRepas


class PlanningRepas:
    """
    Représente un planning de repas sur plusieurs jours.
    """

    def __init__(self, id_utilisateur: int, nom: str, nb_jours: int):
        if nb_jours <= 0:
            raise ValueError("Un planning doit contenir au moins 1 jour")

        self.id = None
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.nb_jours = nb_jours

        self.jours = [JourRepas(numero_jour=i) for i in range(1, nb_jours + 1)]

    def get_jour(self, numero_jour: int) -> JourRepas:
        if numero_jour < 1 or numero_jour > self.nb_jours:
            raise ValueError("Jour invalide")
        return self.jours[numero_jour - 1]

    def est_complet(self) -> bool:
        """
        Vérifie que tous les repas sont renseignés.
        """
        for jour in self.jours:
            for plat in jour.to_dict().values():
                if plat is None:
                    return False
        return True

    def __str__(self):
        return f"PlanningRepas(id={self.id}, nom={self.nom}, nb_jours={self.nb_jours})"
