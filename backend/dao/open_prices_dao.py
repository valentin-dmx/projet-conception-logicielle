import requests


class OpenPricesDao:
    BASE_URL = "https://prices.openfoodfacts.org/api/v1"

    def __init__(self):
        self.session = requests.Session()

    def trouver_code_produit(self, nom_produit: str) -> str | None:
        url = f"{self.BASE_URL}/products"
        params = {"search": nom_produit, "size": 1}

        r = self.session.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()

        items = data.get("items", [])
        if not items:
            return None

        return items[0].get("code")

    def obtenir_prix_par_code(self, code_produit: str) -> tuple[float, str] | None:
        url = f"{self.BASE_URL}/prices"
        params = {"product_code": code_produit, "size": 1}

        r = self.session.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()

        items = data.get("items", [])
        if not items:
            return None

        item = items[0]
        prix = item.get("price")
        devise = item.get("currency")

        if prix is None or devise is None:
            return None

        return float(prix), str(devise)
