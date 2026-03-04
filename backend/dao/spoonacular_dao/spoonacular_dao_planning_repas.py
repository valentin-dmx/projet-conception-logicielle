from backend.business_object.jour_repas import JourRepas
from backend.business_object.planning_repas import PlanningRepas
from backend.dao.spoonacular_dao.spoonacular_dao import SpoonacularDAO


class SpoonacularDAOPlanningRepas(SpoonacularDAO):
    """
    Data Access Object (DAO) pour interagir avec l'API Spoonacular spécifiquement pour les plannings de repas.
    Fournit des méthodes pour créer et gérer les plannings de repas.
    """

    def __init__(self):
        self.dao = SpoonacularDAO()

    def generer_planning(
        self,
        id_utilisateur: int,
        nb_jours: int,
        nom: str = None,
        calories: int = None,
        regime: str = None,
    ) -> PlanningRepas:

        if nb_jours <= 0:
            raise ValueError("nb_jours doit être > 0")

        planning = PlanningRepas(
            id_utilisateur=id_utilisateur, nb_jours=nb_jours, nom=nom
        )

        for num_jour in range(1, nb_jours + 1):
            params = {"timeFrame": "day"}

            if calories:
                params["targetCalories"] = calories

            if regime:
                params["diet"] = regime

            data = self.dao._get("/mealplanner/generate", params=params)

            jour = JourRepas(
                numero_jour=num_jour,
                repas=data["meals"],
                nutriments=data["nutrients"],
            )

            planning.jours.append(jour)

        return planning
