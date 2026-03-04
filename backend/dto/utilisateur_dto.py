from pydantic import BaseModel, Field


class UtilisateurCreateDTO(BaseModel):
    """DTO utilisé pour la création d'un utilisateur"""

    nom_utilisateur: str = Field(..., min_length=3, max_length=50)
    mot_de_passe: str = Field(..., min_length=6)


class UtilisateurConnectDTO(BaseModel):
    """DTO utilisé pour l'authentification d'un utilisateur"""

    nom_utilisateur: str
    mot_de_passe: str


class UtilisateurResponseDTO(BaseModel):
    """DTO retourné au client (sans mot de passe)"""

    id: int
    nom_utilisateur: str

    class Config:
        from_attributes = True  # Permet de créer le DTO depuis un objet métier
