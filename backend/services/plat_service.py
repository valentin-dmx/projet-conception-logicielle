from backend.business_object.ingredient import Ingredient
from backend.business_object.plat import Plat
from backend.dao.spoonacular_dao.spoonacular_dao_plat import SpoonacularDAOPlat


# from backend.services.historique_service import HistoriqueService


class PlatService(SpoonacularDAOPlat):
    """
    Service de gestion des plats.
    """

    def __init__(self, dao=None):
        self.dao = dao or SpoonacularDAOPlat()
        # self.historique_service = historique_service or HistoriqueService()
        # en argument: historique_service=None

    def rechercher_plat_nom(self, requete: str) -> list[Plat]:
        """
        Recherche des plats par leur nom.

        Params
        ----------
            requete: str
                La requête de recherche du plat.
        Return
        ----------
            list[Plat]
                Une liste de plats correspondant à la requête.
        """
        plats_dto = self.dao.recherche_plat_nom(requete)
        plats = [Plat(id=plat_dto.id, nom=plat_dto.nom) for plat_dto in plats_dto]
        id_plats = [plat.id for plat in plats]

        self.historique_service.ajouter_recherche_plat(requete, id_plats)
        return plats

    def information_plat(self, plat_id: int) -> Plat:
        """
        Récupère les informations d'un plat à partir de son ID.

        Params
        ----------
            plat_id: int
                L'ID du plat à récupérer.
        Return
        ----------
            Plat
                Le plat correspondant à l'ID fourni.
        """
        plat_dto = self.dao.information_plat(plat_id)
        plat = Plat(id=plat_dto.id, nom=plat_dto.nom)

        return plat

    def plat_ingredients(self, plat_id: int) -> list[Ingredient]:
        """
        Récupère les ingrédients d'un plat à partir de son ID.

        Params
        ----------
            plat_id: int
                L'ID du plat dont on veut récupérer les ingrédients.
        Return
        ----------
            list[Ingredient]
                Une liste d'ingrédients correspondant au plat fourni.
        """
        ingredients_dto = self.dao.get_plat_ingredients(plat_id)

        return [
            Ingredient(
                id=ing_dto.id,
                nom=ing_dto.nom,
                quantite=ing_dto.quantite,
                unite=ing_dto.unite,
            )
            for ing_dto in ingredients_dto
        ]
