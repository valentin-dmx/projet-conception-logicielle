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
        # clé = (nom normalisé, unité)
        agregation: dict[tuple[str, str], float] = {}

        for ingredient in ingredients:
            nom = str(ingredient["nom"]).strip().lower()
            unite = str(ingredient["unite"]).strip().lower()
            quantite = float(ingredient["quantite"])

            cle = (nom, unite)
            agregation[cle] = agregation.get(cle, 0.0) + quantite

        articles = [
            ArticleCoursesDto(nom=nom, quantite=quantite, unite=unite)
            for (nom, unite), quantite in agregation.items()
        ]

        articles.sort(key=lambda a: (a.nom, a.unite))

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