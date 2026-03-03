class Ingredient:
    """
    Ingrédient métier : nom + quantité + unité
    """

    def __init__(self, nom: str, quantite: float, unite: str):
        self.nom = str(nom).strip().lower()
        self.quantite = float(quantite)
        self.unite = str(unite).strip().lower()

    def cle_agregation(self) -> tuple[str, str]:
        return (self.nom, self.unite)

    def ajouter(self, autre: "Ingredient") -> None:
        """
        Additionne la quantité d'un ingrédient identique (même nom + unité).
        """
        if self.cle_agregation() != autre.cle_agregation():
            raise ValueError("Impossible d'additionner deux ingrédients différents.")
        self.quantite += autre.quantite

    def soustraire(self, autre: "Ingredient") -> "Ingredient":
        """
        Retourne ce qu'il reste à acheter après retrait du stock (autre).
        """
        if self.cle_agregation() != autre.cle_agregation():
            raise ValueError("Impossible de soustraire deux ingrédients différents.")
        reste = self.quantite - autre.quantite
        if reste < 0:
            reste = 0.0
        return Ingredient(self.nom, reste, self.unite)

    def __str__(self) -> str:
        return (
            f"Ingredient(nom={self.nom}, quantite={self.quantite}, unite={self.unite})"
        )
