from business_object.ingredient import Ingredient
from business_object.inventaire import Inventaire


class ListeCourses:
    """
    Liste de courses métier.
    - agrège les ingrédients
    - calcule ce qu'il reste à acheter selon un inventaire
    """

    def __init__(self):
        self._ingredients: dict[tuple[str, str], Ingredient] = {}

    def ajouter_ingredient(self, ingredient: Ingredient) -> None:
        cle = ingredient.cle_agregation()
        if cle in self._ingredients:
            self._ingredients[cle].ajouter(ingredient)
        else:
            self._ingredients[cle] = Ingredient(
                ingredient.nom, ingredient.quantite, ingredient.unite
            )

    def ingredients(self) -> list[Ingredient]:
        res = list(self._ingredients.values())
        res.sort(key=lambda i: (i.nom, i.unite))
        return res

    def calculer_a_acheter(self, inventaire: Inventaire) -> "ListeCourses":
        """
        Retourne une nouvelle ListeCourses avec uniquement ce qui manque.
        """
        resultat = ListeCourses()

        for ing in self.ingredients():
            dispo = inventaire.obtenir_ingredient(ing.nom, ing.unite)
            if dispo is None:
                resultat.ajouter_ingredient(ing)
            else:
                reste = ing.soustraire(dispo)
                if reste.quantite > 0:
                    resultat.ajouter_ingredient(reste)

        return resultat

    def __str__(self) -> str:
        contenu = [str(i) for i in self.ingredients()]
        return f"ListeCourses(ingredients={contenu})"
