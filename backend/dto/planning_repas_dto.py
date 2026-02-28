from pydantic import BaseModel

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
        return cls(
            id_utilisateur=planning_repas.id_utilisateur,
            id=planning_repas.id,
            nom=planning_repas.nom,
            nb_jours=planning_repas.nb_jours,
            jours=[JourRepasDTO.from_jour_repas(jour) for jour in planning_repas.jours],
        )

    def to_planning_repas(self) -> "PlanningRepas":
        planning_repas = PlanningRepas(
            id_utilisateur=self.id_utilisateur,
            id=self.id,
            nom=self.nom,
            nb_jours=self.nb_jours,
        )
        planning_repas.jours = [jour_dto.to_jour_repas() for jour_dto in self.jours]
        return planning_repas
