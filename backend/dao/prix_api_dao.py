from backend.dao.open_prices_dao import OpenPricesDao


class PrixApiDao:
    def __init__(self):
        self.open_prices = OpenPricesDao()

    def obtenir_prix(self, nom_produit: str) -> tuple[float, str] | None:
        code = self.open_prices.trouver_code_produit(nom_produit)
        if not code:
            return None

        return self.open_prices.obtenir_prix_par_code(code)
