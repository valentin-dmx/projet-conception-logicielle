class Plat:
    """
    Classe représentant un plat.
    """

    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    def __str__(self):
        return f"Plat(id={self.id}, nom={self.nom})"
