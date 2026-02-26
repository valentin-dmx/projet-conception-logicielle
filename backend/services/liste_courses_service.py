from backend.business_object.ingredient import Ingredient
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
    ) -> ListeCoursesDto:
        # 1) Logique métier (agrégation) dans le BO
        liste_bo = ListeCourses()

        for ingredient in ingredients:
            liste_bo.ajouter_ingredient(
                Ingredient(
                    nom=ingredient["nom"],
                    quantite=ingredient["quantite"],
                    unite=ingredient["unite"],
                )
            )

        # 2) Conversion BO -> DTO
        articles = [
            ArticleCoursesDto(nom=i.nom, quantite=i.quantite, unite=i.unite)
            for i in liste_bo.ingredients()
        ]

        # 3) Estimation coût total via API (orchestration dans le service)
        total = 0.0
        if activer_prix:
            for article in articles:
                res = self.prix_api.obtenir_prix(article.nom)
                if res is None:
                    continue

                prix, devise = res  # devise pas utilisée pour l’instant
                article.prix_estime = prix
                total += prix

            return ListeCoursesDto(articles=articles, cout_total_estime=total)

        return ListeCoursesDto(articles=articles, cout_total_estime=None)
