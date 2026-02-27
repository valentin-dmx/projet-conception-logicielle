import os

import requests

from backend.dto.ingredient_dto import IngredientDTO
from backend.dto.plat_dto import PlatDTO


class SpoonacularDAO:
    BASE_URL = "https://api.spoonacular.com"

    def __init__(self):
        self.api_key = os.environ.get("SPOONACULAR_API_KEY")
        if not self.api_key:
            raise RuntimeError("Variable d'environnement SPOONACULAR_API_KEY manquante")

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}

        params["apiKey"] = self.api_key

        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=10)

        response.raise_for_status()
        return response.json()

    def recherche_plat_nom(self, query, number=2):
        data = self._get("/recipes/complexSearch", {"query": query, "number": number})

        return [
            PlatDTO(id=plat["id"], nom=plat["title"])
            for plat in data.get("results", [])
        ]

    def information_plat(self, recipe_id):
        data = self._get(
            f"/recipes/{recipe_id}/information", {"includeNutrition": False}
        )

        return PlatDTO(id=data["id"], nom=data["title"])

    def get_plat_ingredients(self, recipe_id):
        data = self._get(
            f"/recipes/{recipe_id}/information", {"includeNutrition": False}
        )

        return [
            IngredientDTO(
                id=ing["id"], nom=ing["name"], quantite=ing["amount"], unite=ing["unit"]
            )
            for ing in data.get("extendedIngredients", [])
        ]
