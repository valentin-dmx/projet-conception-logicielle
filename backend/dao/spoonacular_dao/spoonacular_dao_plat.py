from backend.dao.spoonacular_dao.spoonacular_dao import SpoonacularDAO
from backend.dto.ingredient_dto import IngredientDTO
from backend.dto.plat_dto import PlatDTO


class SpoonacularDAOPlat(SpoonacularDAO):
    """
    Data Access Object (DAO) pour interagir avec l'API Spoonacular spécifiquement pour les plats.
    Fournit des méthodes pour rechercher des plats, récupérer leurs informations et leurs ingrédients."""

    NOMBRE_RESULTATS = 2

    def recherche_plat_nom(self, query, number=NOMBRE_RESULTATS):
        """
        Recherche des plats par leur nom.

        Params
        ------------
            query: str
                La requête de recherche du plat.
            number: int
                Le nombre de résultats à retourner (par défaut: NOMBRE_RESULTATS).
        Return
        ------------
            list[PlatDTO]
                Une liste de plats correspondant à la requête.
        """
        data = self._get("/recipes/complexSearch", {"query": query, "number": number})

        return [
            PlatDTO(id=plat["id"], nom=plat["title"])
            for plat in data.get("results", [])
        ]

    def information_plat(self, plat_id):
        """
        Récupère les informations d'un plat à partir de son ID.

        Params
        ------------
            plat_id: int
                L'ID du plat à récupérer.
        Return
        ------------
            PlatDTO
                Le plat correspondant à l'ID fourni.
        """
        data = self._get(f"/recipes/{plat_id}/information", {"includeNutrition": False})

        return PlatDTO(id=data["id"], nom=data["title"])

    def get_plat_ingredients(self, recipe_id):
        """
        Récupère les ingrédients d'un plat à partir de son ID.

        Params
        ------------
            recipe_id: int
                L'ID du plat dont on veut récupérer les ingrédients.
        Return
        ------------
            list[IngredientDTO]
                Une liste d'ingrédients correspondant au plat fourni.
        """
        data = self._get(
            f"/recipes/{recipe_id}/information", {"includeNutrition": False}
        )

        return [
            IngredientDTO(
                id=ing["id"], nom=ing["name"], quantite=ing["amount"], unite=ing["unit"]
            )
            for ing in data.get("extendedIngredients", [])
        ]
