from pydantic import BaseModel

from backend.business_object.jour_repas import JourRepas
from backend.business_object.planning_repas import PlanningRepas
from backend.dto.jour_repas_dto import JourRepasDTO


class PlanningRepasDTO(BaseModel):
    """
    DTO représentant un planning de repas sur plusieurs jours.
    """

    id_utilisateur: int = None
    nb_jours: int
    jours: list[JourRepasDTO]
    id: int = None
    nom: str = None

    @classmethod
    def from_planning_repas(cls, planning_repas: PlanningRepas) -> "PlanningRepasDTO":
        jours_dto = []
        for i in range(1, planning_repas.nb_jours + 1):
            jour = getattr(planning_repas, f"jour_{i}")
            jour_dto = JourRepasDTO(
                petit_dejeuner=jour.petit_dejeuner,
                dejeuner=jour.dejeuner,
                diner=jour.diner,
            )
            jours_dto.append(jour_dto)
        return PlanningRepasDTO(
            id_utilisateur=planning_repas.id_utilisateur,
            id=planning_repas.id,
            nom=planning_repas.nom,
            nb_jours=planning_repas.nb_jours,
            jours=jours_dto,
        )

    def to_planning_repas(self) -> "PlanningRepas":
        planning_repas = PlanningRepas(
            id_utilisateur=self.id_utilisateur,
            id=self.id,
            nom=self.nom,
            nb_jours=self.nb_jours,
        )
        for i, jour_dto in enumerate(self.jours, start=1):
            jour = JourRepas(
                petit_dejeuner=jour_dto.petit_dejeuner,
                dejeuner=jour_dto.dejeuner,
                diner=jour_dto.diner,
            )
            setattr(planning_repas, f"jour_{i}", jour)
        return planning_repas
