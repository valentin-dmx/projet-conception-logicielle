from pydantic import BaseModel


class PlatDTO(BaseModel):
    id: int
    nom: str
