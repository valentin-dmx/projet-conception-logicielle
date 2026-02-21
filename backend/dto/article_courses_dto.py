class ArticleCoursesDto:
    def __init__(self, nom: str, quantite: float, unite: str, prix_estime: float | None = None):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite
        self.prix_estime = prix_estime
