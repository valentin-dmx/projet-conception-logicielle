from backend.dto.ingredient_dto import IngredientDTO


class ListeCoursesDto:
    def __init__(
        self, articles: list[IngredientDTO], cout_total_estime: float | None = None
    ):
        self.articles = articles
        self.cout_total_estime = cout_total_estime
