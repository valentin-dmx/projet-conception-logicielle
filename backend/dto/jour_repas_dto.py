from pydantic import BaseModel


class JourRepasDTO(BaseModel):
    """
    DTO représentant les repas d’un jour.
    """

    petit_dejeuner: str | None = None
    dejeuner: str | None = None
    diner: str | None = None
