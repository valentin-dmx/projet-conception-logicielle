from backend.dto.liste_courses_dto import ListeCoursesDto
from backend.dto.article_courses_dto import ArticleCoursesDto


class ListeCoursesService:
    def generer_liste_courses(self, ingredients: list[dict]) -> ListeCoursesDto:
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

        return ListeCoursesDto(articles=articles)