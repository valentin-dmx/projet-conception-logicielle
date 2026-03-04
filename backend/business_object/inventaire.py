from business_object.ingredient import Ingredient


class Inventaire:
    """
    Inventaire métier : ingrédients déjà disponibles chez l'utilisateur.
    """

    def __init__(self):
        self._stock: dict[tuple[str, str], Ingredient] = {}

    def ajouter_ingredient(self, ingredient: Ingredient) -> None:
        cle = ingredient.cle_agregation()
        if cle in self._stock:
            self._stock[cle].ajouter(ingredient)
        else:
            self._stock[cle] = Ingredient(
                ingredient.nom, ingredient.quantite, ingredient.unite
            )

    def obtenir_ingredient(self, nom: str, unite: str) -> Ingredient | None:
        cle = (str(nom).strip().lower(), str(unite).strip().lower())
        return self._stock.get(cle)

    def __str__(self) -> str:
        contenu = [str(i) for i in self._stock.values()]
        return f"Inventaire(stock={contenu})"
