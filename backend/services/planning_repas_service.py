from business_object.planning_repas import PlanningRepas
from dao.planning_dao import PlanningDAO
from dao.spoonacular_dao.spoonacular_dao_planning_repas import (
    SpoonacularDAOPlanningRepas,
)
from dto.planning_repas_dto import PlanningRepasDTO


MOMENTS = ["petit_dejeuner", "dejeuner", "diner"]


class PlanningRepasService:
    """
    Service pour gérer les plannings de repas.
    """

    def __init__(self):
        self.planning_repas_dao = PlanningDAO()
        self.spoonacular_dao = SpoonacularDAOPlanningRepas()

    def creer_planning_repas(self, nb_jours: int) -> PlanningRepas:
        """
        Crée un nouveau planning de repas avec le nombre de jours spécifié.
        Params
        ----------
            nb_jours: int
                Le nombre de jours pour le planning de repas.
        Return
        ----------
            PlanningRepas
                Le planning de repas créé.
        """
        planning_dto = self.spoonacular_dao.generer_planning(nb_jours)
        planning_repas = PlanningRepasDTO.dto_to_bo(planning_dto)
        return planning_repas

    def creer_planning_repas_utilisateur(
        self, id_utilisateur: int, nb_jours: int, nom_planning: str = None
    ) -> "PlanningRepas":
        """
        Crée un nouveau planning de repas pour un utilisateur avec le nom et le nombre de jours spécifiés.
        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur pour lequel créer le planning de repas.
            nb_jours: int
                Le nombre de jours pour le planning de repas.
            nom_planning: str, optional
                Le nom du planning de repas (par défaut: None).
        Return
        ----------
                PlanningRepas
                    Le planning de repas créé.
        """
        planning_dto = self.spoonacular_dao.generer_planning(nb_jours)
        planning_repas = PlanningRepasDTO.dto_to_bo(planning_dto)

        planning_repas.id_utilisateur = id_utilisateur
        if nom_planning:
            planning_repas.nom = nom_planning

        planning_sauvegarde = (
            self.planning_repas_dao.ajouter_planning_repas_utilisateur(planning_repas)
        )

        return planning_sauvegarde

    def compter_plannings_repas_utilisateur(self, id_utilisateur: int) -> int:
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
        nb_plannings: int = self.planning_repas_dao.compter_plannings_repas_utilisateur(
            id_utilisateur
        )
        return nb_plannings

    def voir_planning_repas(
        self, id_utilisateur: int, id_planning: int
    ) -> PlanningRepas:
        """
        Récupère un planning de repas par son ID.
        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            id_planning: int
                L'ID du planning de repas à récupérer.
        Return
        ----------
            PlanningRepas
                Le planning de repas correspondant à l'ID fourni.
        """
        planning_repas: PlanningRepas = self.planning_repas_dao.voir_planning_repas(
            id_utilisateur, id_planning
        )
        return planning_repas

    def voir_tous_planning_repas_utilisateur(
        self, id_utilisateur: int
    ) -> list[PlanningRepas]:
        """
        Récupère tous les plannings de repas associés à un utilisateur.
        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur dont on veut récupérer les plannings de repas.
        Return
        ----------
            list[PlanningRepas]
                Une liste de plannings de repas associés à l'utilisateur fourni.
        """
        plannings_repas: list[PlanningRepas] = (
            self.planning_repas_dao.voir_tous_planning_repas_utilisateur(id_utilisateur)
        )
        return plannings_repas

    def modifier_planning_repas_utilisateur(
        self,
        id_utilisateur: int,
        planning_id: int,
        jour_modif: int,
        moment_modif: str,
        id_plat_modif: int,
    ) -> "PlanningRepas":
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
                Le moment de la journée du planning de repas à modifier (ex: "petit_dejeuner", "dejeuner", "diner").
            id_plat_modif: int
                L'ID du plat à associer au jour et moment modifiés du planning de repas.
        Return
        ----------
                PlanningRepas
                    Le planning de repas modifié.
        """

        if moment_modif not in MOMENTS:
            raise ValueError(
                "Moment de la journée invalide. Doit être 'petit_dejeuner', 'dejeuner' ou 'diner'."
            )

        planning_repas_dto = (
            self.planning_repas_dao.modifier_planning_repas_utilisateur(
                id_utilisateur, planning_id, jour_modif, moment_modif, id_plat_modif
            )
        )
        planning_repas = PlanningRepasDTO.dto_to_bo(planning_repas_dto)
        return planning_repas

    def supprimer_planning_repas_utilisateur(
        self, id_utilisateur: int, planning_id: int
    ) -> None:
        """
        Supprime un planning de repas existant pour un utilisateur.
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
        self.planning_repas_dao.supprimer_planning_repas_utilisateur(
            id_utilisateur, planning_id
        )

    def ajouter_jour_planning_repas_utilisateur(
        self, id_utilisateur: int, planning_id: int
    ) -> "PlanningRepas":
        """
        Ajoute un jour à un planning de repas existant pour un utilisateur.
        """
        planning_repas_dto = (
            self.planning_repas_dao.ajouter_jour_planning_repas_utilisateur(
                id_utilisateur, planning_id
            )
        )
        planning_repas = PlanningRepasDTO.dto_to_bo(planning_repas_dto)
        return planning_repas

    def supprimer_jour_planning_repas_utilisateur(
        self, id_utilisateur: int, planning_id: int
    ) -> "PlanningRepas":
        """
        Supprime un jour d'un planning de repas existant pour un utilisateur.
        """
        planning_repas_dto = (
            self.planning_repas_dao.supprimer_jour_planning_repas_utilisateur(
                id_utilisateur, planning_id
            )
        )
        planning_repas = PlanningRepasDTO.dto_to_bo(planning_repas_dto)
        return planning_repas

    def renommer_planning_repas_utilisateur(
        self, id_utilisateur: int, planning_id: int, nouveau_nom: str
    ) -> None:
        """
        Renomme un planning de repas existant pour un utilisateur.
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
        self.planning_repas_dao.renommer_planning_repas_utilisateur(
            id_utilisateur, planning_id, nouveau_nom
        )
