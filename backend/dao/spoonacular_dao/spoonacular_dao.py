import os

import requests


class SpoonacularDAO:
    """
    Data Access Object (DAO) pour interagir avec l'API Spoonacular.
    """

    BASE_URL = "https://api.spoonacular.com"

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
