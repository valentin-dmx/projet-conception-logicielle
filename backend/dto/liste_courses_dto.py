from backend.dto.article_courses_dto import ArticleCoursesDto


class ListeCoursesDto:
    def __init__(self, articles: list[ArticleCoursesDto], cout_total_estime: float | None = None):
        self.articles = articles
        self.cout_total_estime = cout_total_estime
