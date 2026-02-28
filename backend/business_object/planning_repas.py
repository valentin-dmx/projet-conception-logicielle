from backend.business_object.jour_repas import JourRepas


class PlanningRepas:
    """
    Classe représentant un planning de repas sur plusieurs jours.
    Chaque jour est représenté par une instance de JourRepas.
    """

    def __init__(self, id_utilisateur=None, id=None, nom=None, nb_jours=None):
        self.id_utilisateur = id_utilisateur
        self.id = id
        self.nom = nom
        self.nb_jours = nb_jours
        self.jours = []
        for i in range(1, nb_jours + 1):
            self.jours.append(JourRepas(id_utilisateur, id, nom, i))

    def __str__(self):
        return f"PlanningRepas(id_utilisateur={self.id_utilisateur}, id={self.id}, nom={self.nom}, nb_jours={self.nb_jours}, jours={self.jours})"
