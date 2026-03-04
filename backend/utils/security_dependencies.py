from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from dao.exceptions import InvalidPasswordError, NotFoundError
from services.utilisateur_service import UtilisateurService


security = HTTPBasic()


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),  # noqa: B008
):
    service = UtilisateurService.of_context()

    try:
        utilisateur = service.authentifier(
            nom_utilisateur=credentials.username,
            mot_de_passe=credentials.password,
        )
        return utilisateur

    except (InvalidPasswordError, NotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        ) from e


def get_current_admin(user=Depends(get_current_user)):  # noqa: B008
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs",
        )
    return user
