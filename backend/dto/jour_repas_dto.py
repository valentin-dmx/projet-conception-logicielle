from pydantic import BaseModel

from backend.business_object.jour_repas import JourRepas


class JourRepasDTO(BaseModel):
    """
    DTO représentant les repas d’un jour.
    """

    petit_dejeuner: str = None
    dejeuner: str = None
    diner: str = None

    @classmethod
    def from_jour_repas(cls, jour_repas: JourRepas) -> "JourRepasDTO":
        return cls(
            petit_dejeuner=jour_repas.petit_dejeuner,
            dejeuner=jour_repas.dejeuner,
            diner=jour_repas.diner,
        )

    def to_jour_repas(self) -> "JourRepas":
        return JourRepas(
            petit_dejeuner=self.petit_dejeuner, dejeuner=self.dejeuner, diner=self.diner
        )
