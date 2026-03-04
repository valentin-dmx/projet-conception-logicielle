from fastapi import APIRouter, HTTPException, status

from business_object.utilisateur import Utilisateur
from dao.exceptions import (
    DatabaseCreationError,
    InvalidPasswordError,
    NotFoundError,
)
from dao.utilisateur_dao import UtilisateurDao
from dto.utilisateur_dto import (
    UtilisateurConnectDTO,
    UtilisateurCreateDTO,
    UtilisateurResponseDTO,
)


utilisateur_router = APIRouter(
    prefix="/utilisateurs",
    tags=["utilisateurs"],
)


@utilisateur_router.post(
    "/",
    response_model=UtilisateurResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def creer_utilisateur(utilisateur_dto: UtilisateurCreateDTO):
    """Créer un nouvel utilisateur"""
    utilisateur_dao = UtilisateurDao()

    # Vérifier si le nom d'utilisateur existe déjà
    if utilisateur_dao.verifier_nom_utilisateur_existant(
        utilisateur_dto.nom_utilisateur
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Le nom d'utilisateur existe déjà.",
        )

    utilisateur = Utilisateur(
        id=None,
        nom_utilisateur=utilisateur_dto.nom_utilisateur,
    )

    try:
        utilisateur_dao.creer(
            utilisateur=utilisateur,
            mot_de_passe=utilisateur_dto.mot_de_passe,
        )
    except DatabaseCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return utilisateur


@utilisateur_router.post("/connect", response_model=UtilisateurResponseDTO)
def se_connecter(utilisateur_dto: UtilisateurConnectDTO):
    """Authentifier un utilisateur"""
    utilisateur_dao = UtilisateurDao()

    try:
        utilisateur = utilisateur_dao.se_connecter(
            nom_utilisateur=utilisateur_dto.nom_utilisateur,
            mot_de_passe=utilisateur_dto.mot_de_passe,
        )
        return utilisateur

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e


@utilisateur_router.get("/", response_model=list[UtilisateurResponseDTO])
def lister_utilisateurs():
    """Lister tous les utilisateurs"""
    utilisateur_dao = UtilisateurDao()
    return utilisateur_dao.lister_tous()


@utilisateur_router.get("/{id}", response_model=UtilisateurResponseDTO)
def trouver_utilisateur_par_id(id: int):
    """Trouver un utilisateur par son identifiant"""
    utilisateur_dao = UtilisateurDao()
    utilisateur = utilisateur_dao.trouver_par_id(id)

    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé.",
        )

    return utilisateur


@utilisateur_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_utilisateur(id: int):
    """Supprimer un utilisateur"""
    utilisateur_dao = UtilisateurDao()

    if not utilisateur_dao.verifier_id_existant(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé.",
        )

    utilisateur_dao.supprimer(id)
    return None
