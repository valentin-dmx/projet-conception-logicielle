from backend.business_object.planning_repas import PlanningRepas
from backend.dto.jour_repas_dto import JourRepasDTO


class PlanningRepasDTO:
    """
    DTO pour le planning de repas.
    """

    def __init__(
        self,
        id_utilisateur: int,
        nom: str,
        nb_jours: int,
        jours: list[JourRepasDTO],
        id: int | None = None,
    ):
        self.id = id
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.nb_jours = nb_jours
        self.jours = jours

    @staticmethod
    def dto_to_bo(dto: "PlanningRepasDTO") -> PlanningRepas:
        planning = PlanningRepas(
            id_utilisateur=dto.id_utilisateur, nom=dto.nom, nb_jours=dto.nb_jours
        )

        for jour_dto in dto.jours:
            jour_bo = planning.get_jour(jour_dto.numero_jour)
            jour_bo.petit_dejeuner = jour_dto.petit_dejeuner
            jour_bo.dejeuner = jour_dto.dejeuner
            jour_bo.diner = jour_dto.diner

        return planning

    @staticmethod
    def bo_to_dto(planning: PlanningRepas) -> "PlanningRepasDTO":

        jours_dto = []

        for jour in planning.jours:
            jours_dto.append(
                JourRepasDTO(
                    numero_jour=jour.numero_jour,
                    petit_dejeuner=jour.petit_dejeuner,
                    dejeuner=jour.dejeuner,
                    diner=jour.diner,
                )
            )

        return PlanningRepasDTO(
            id=planning.id,
            id_utilisateur=planning.id_utilisateur,
            nom=planning.nom,
            nb_jours=planning.nb_jours,
            jours=jours_dto,
        )
