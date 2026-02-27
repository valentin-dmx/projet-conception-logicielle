import os

import requests

from backend.dto.ingredient_dto import IngredientDTO
from backend.dto.plat_dto import PlatDTO


class SpoonacularDAOPlat(SpoonacularDAO):
    """
    Data Access Object (DAO) pour interagir avec l'API Spoonacular spécifiquement pour les plats.
    Fournit des méthodes pour rechercher des plats, récupérer leurs informations et leurs ingrédients."""

    NOMBRE_RESULTATS = 2
=======

class SpoonacularDAO:
    BASE_URL = "https://api.spoonacular.com"
>>>>>>> develop

    def __init__(self):
        self.api_key = os.environ.get("SPOONACULAR_API_KEY")
        if not self.api_key:
            raise RuntimeError("Variable d'environnement SPOONACULAR_API_KEY manquante")

    def _get(self, endpoint, params=None):
        """
        Effectue une requête GET à l'API Spoonacular.

        Params
        ------------
            endpoint: str
                Le point de terminaison de l'API à appeler.
            params: dict, optional
                Les paramètres de la requête (par défaut: None).
        Return
        ------------
            dict
                La réponse de l'API sous forme de dictionnaire.
        """
        if params is None:
            params = {}

        params["apiKey"] = self.api_key

        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=10)

        response.raise_for_status()
        return response.json()

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
=======
    def recherche_plat(self, query, number=2):
        return self._get("/recipes/complexSearch", {"query": query, "number": number})

    def get_plat_ingredients(self, recipe_id):
>>>>>>> develop
        data = self._get(
            f"/recipes/{recipe_id}/information", {"includeNutrition": False}
        )

        return [
<<<<<<< plat
            IngredientDTO(
                id=ing["id"], nom=ing["name"], quantite=ing["amount"], unite=ing["unit"]
            )
            for ing in data.get("extendedIngredients", [])
=======
            {"name": i["name"], "amount": i["amount"], "unit": i["unit"]}
            for i in data.get("extendedIngredients", [])
>>>>>>> develop
        ]
