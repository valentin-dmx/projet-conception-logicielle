from backend.business_object.ingredient import Ingredient
from backend.business_object.inventaire import Inventaire
from backend.business_object.liste_courses import ListeCourses
from backend.dao.prix_api_dao import PrixApiDao
from backend.dto.article_courses_dto import ArticleCoursesDto
from backend.dto.liste_courses_dto import ListeCoursesDto


class ListeCoursesService:
    def __init__(self):
        self.prix_api = PrixApiDao()

    def generer_liste_courses(
        self,
        ingredients: list[dict],
        activer_prix: bool = True,
        disponibles: list[dict] | None = None,
    ) -> ListeCoursesDto:
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
            ArticleCoursesDto(nom=i.nom, quantite=i.quantite, unite=i.unite)
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
            prix, devise = res  # devise pas utilisée pour l’instant
            article.prix_estime = prix
            total += prix

        return ListeCoursesDto(articles=articles, cout_total_estime=total)
