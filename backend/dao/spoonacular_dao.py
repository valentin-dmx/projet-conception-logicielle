import os

import requests


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

    def recherche_plat(self, query, number=2):
        return self._get("/recipes/complexSearch", {"query": query, "number": number})

    def get_plat_ingredients(self, recipe_id):
        data = self._get(
            f"/recipes/{recipe_id}/information", {"includeNutrition": False}
        )

        return [
            {"name": i["name"], "amount": i["amount"], "unit": i["unit"]}
            for i in data.get("extendedIngredients", [])
        ]
