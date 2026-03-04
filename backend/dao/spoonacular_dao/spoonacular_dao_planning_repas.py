from dao.spoonacular_dao.spoonacular_dao import SpoonacularDAO
from dto.planning_repas_dto import PlanningRepasDTO


class SpoonacularDAOPlanningRepas(SpoonacularDAO):
    """
    Data Access Object (DAO) pour interagir avec l'API Spoonacular spécifiquement pour les plannings de repas.
    Fournit des méthodes pour créer et gérer les plannings de repas.
    """

    def creer_planning_repas(
        self, nb_jours, id_utilisateur=None, vide: bool = False
    ) -> PlanningRepasDTO:
        """
        Crée un nouveau planning de repas avec le nombre de jours spécifié.
        Params
        ----------
            nb_jours: int
                Le nombre de jours pour le planning de repas.
            id_utilisateur: int, optional
                L'ID de l'utilisateur auquel le planning de repas est associé (par défaut: None).
            vide: bool, optional
                Indique si le planning de repas doit être créé vide (par défaut: None).
        Return
        ----------
            PlanningRepasDTO
                Le DTO représentant le planning de repas créé.
        """
        pass

    def compter_planning_repas_utilisateur(self, id_utilisateur: int) -> int:
        """
        Compte le nombre de plannings de repas associés à un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur dont on veut compter les plannings de repas.
        Return
        ----------
            int
                Le nombre de plannings de repas associés à l'utilisateur fourni.
        """
        pass

    def voir_planning_repas(
        self, id_utilisateur: int, id_planning: int
    ) -> PlanningRepasDTO:
        """
        Récupère un planning de repas par son ID.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à récupérer.
        Return
        ----------
            PlanningRepasDTO
                Le DTO représentant le planning de repas correspondant à l'ID fourni.
        """
        pass

    def voir_tous_planning_repas_utilisateur(
        self, id_utilisateur: int
    ) -> list[PlanningRepasDTO]:
        """
        Récupère tous les plannings de repas associés à un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur dont on veut récupérer les plannings de repas.
        Return
        ----------
            list[PlanningRepasDTO]
                Une liste de DTO représentant tous les plannings de repas associés à l'utilisateur fourni.
        """
        pass

    def renommer_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int, nouveau_nom: str
    ) -> None:
        """
        Renomme un planning de repas pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à renommer.
            nouveau_nom: str
                Le nouveau nom à attribuer au planning de repas.
        Return
        ----------
            None
        """
        pass

    def supprimer_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int
    ) -> None:
        """
        Supprime un planning de repas pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à supprimer.
        Return
        ----------
            None
        """
        pass

    def modifier_planning_repas_utilisateur(
        self,
        id_utilisateur: int,
        id_planning: int,
        jour_modif: int,
        moment_modif: str,
        id_plat_modif: int,
    ) -> PlanningRepasDTO:
        """
        Modifie un planning de repas existant pour un utilisateur avec les nouvelles informations fournies dans le DTO.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à modifier.
            jour_modif: int
                Le jour du planning de repas à modifier.
            moment_modif: str
                Le moment du jour à modifier (ex: "petit_dejeuner", "dejeuner", "diner").
            id_plat_modif: int
                L'ID du plat à associer au jour et moment modifiés du planning de repas.
        Return
        ----------
            PlanningRepasDTO
                Un DTO représentant le planning de repas modifié pour l'utilisateur.
        """
        pass

    def ajouter_jour_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int
    ) -> PlanningRepasDTO:
        """
        Ajoute un jour à un planning de repas existant pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas auquel ajouter un jour.
        Return
        ----------
            PlanningRepasDTO
                Un DTO représentant le planning de repas modifié avec le jour ajouté pour l'utilisateur.
        """
        pass

    def supprimer_jour_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int
    ) -> PlanningRepasDTO:
        """
        Supprime un jour d'un planning de repas existant pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas auquel supprimer un jour.
        Return
        ----------
            PlanningRepasDTO
                Un DTO représentant le planning de repas modifié avec le jour supprimé pour l'utilisateur.
        """
        pass
