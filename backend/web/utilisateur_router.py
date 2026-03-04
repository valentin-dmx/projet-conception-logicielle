from fastapi import APIRouter, Depends, HTTPException, status

from dao.exceptions import (
    NotFoundError,
    UtilisateurAlreadyExistsError,
)
from dto.utilisateur_dto import (
    UtilisateurCreateDTO,
    UtilisateurResponseDTO,
)
from services.utilisateur_service import UtilisateurService
from utils.security_dependencies import get_current_admin, get_current_user


utilisateur_router = APIRouter(
    prefix="/utilisateurs",
    tags=["Utilisateurs"],
)

# -------------------------
# Création
# -------------------------


@utilisateur_router.post(
    "/",
    response_model=UtilisateurResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def creer_utilisateur(utilisateur_dto: UtilisateurCreateDTO):
    service = UtilisateurService.of_context()

    try:
        utilisateur = service.creer_utilisateur(
            nom_utilisateur=utilisateur_dto.nom_utilisateur,
            mot_de_passe=utilisateur_dto.mot_de_passe,
            role="user",
        )
        return utilisateur

    except UtilisateurAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


# -------------------------
# Lecture
# -------------------------


@utilisateur_router.get(
    "/",
    response_model=list[UtilisateurResponseDTO],
)
def lister_utilisateurs(_=Depends(get_current_user)):  # noqa: B008
    service = UtilisateurService.of_context()
    return service.lister_utilisateurs()


@utilisateur_router.get(
    "/{id}",
    response_model=UtilisateurResponseDTO,
)
def trouver_utilisateur(id: int, _=Depends(get_current_user)):  # noqa: B008
    service = UtilisateurService.of_context()

    try:
        return service.trouver_par_id(id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


# -------------------------
# Suppression
# -------------------------


@utilisateur_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@utilisateur_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def supprimer_utilisateur(
    id: int,
    _=Depends(get_current_admin),  # noqa: B008
):
    service = UtilisateurService.of_context()

    try:
        service.supprimer_utilisateur(id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    return None
