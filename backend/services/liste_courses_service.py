from backend.business_object.ingredient import Ingredient
from backend.business_object.inventaire import Inventaire
from backend.business_object.liste_courses import ListeCourses
from backend.dao.prix_api_dao import PrixApiDao
from backend.dto.ingredient_dto import IngredientDTO
from backend.dto.liste_courses_dto import ListeCoursesDto


class ListeCoursesService:
    """
    Service pour générer une liste de courses.
    """

    def __init__(self):
        """
        Initialise le service et le DAO de prix.
        """
        self.prix_api = PrixApiDao()

    def generer_liste_courses(
        self,
        ingredients: list[dict],
        activer_prix: bool = True,
        disponibles: list[dict] | None = None,
    ) -> ListeCoursesDto:
        """
        Génère une liste de courses à partir des ingrédients fournis, en option en soustrayant
        les ingrédients disponibles (inventaire en fonction des unités)
        et en estimant le coût total.

        Params
        ----------
            ingredients: list[dict]
                Liste d'ingrédients à ajouter à la liste de courses.
                Chaque élément doit contenir "nom", "quantite" et "unite".
            activer_prix: bool, optional
                Active l'estimation des prix via l'API (par défaut: True).
            disponibles: list[dict] | None, optional
                Liste d'ingrédients disponibles dans l'inventaire.
                Si fourni, ces quantités sont soustraites de la liste à acheter (par défaut: None).

        Return
        ----------
            ListeCoursesDto
                DTO contenant la liste des articles à acheter et, si activé, le coût total estimé.
        """
        # 1) BO: construire la liste agrégée depuis le planning
        liste_bo = ListeCourses()
        for ing in ingredients:
            liste_bo.ajouter_ingredient(
                Ingredient(nom=ing["nom"], quantite=ing["quantite"], unite=ing["unite"])
            )

        # 2) BO: soustraire l’inventaire si fourni
        if disponibles:
            inventaire = Inventaire()
            for d in disponibles:
                inventaire.ajouter_ingredient(
                    Ingredient(nom=d["nom"], quantite=d["quantite"], unite=d["unite"])
                )
            liste_bo = liste_bo.calculer_a_acheter(inventaire)

        # 3) Conversion BO -> DTO
        articles = [
            IngredientDTO(nom=i.nom, quantite=i.quantite, unite=i.unite)
            for i in liste_bo.ingredients()
        ]

        # 4) Prix (optionnel)
        if not activer_prix:
            return ListeCoursesDto(articles=articles, cout_total_estime=None)

        total = 0.0
        for article in articles:
            res = self.prix_api.obtenir_prix(article.nom)
            if res is None:
                continue
            prix, devise = res  # devise pas utilisée
            article.prix_estime = prix
            total += prix

        return ListeCoursesDto(articles=articles, cout_total_estime=total)
