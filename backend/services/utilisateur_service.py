from business_object.utilisateur import Utilisateur
from dao.exceptions import (
    DatabaseCreationError,
    DatabaseDeletionError,
    InvalidPasswordError,
    NotFoundError,
    UtilisateurAlreadyExistsError,
)
from dao.utilisateur_dao import UtilisateurDao


class UtilisateurService:
    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()

    @classmethod
    def of_context(cls):
        return cls()

    # -------------------------
    # Création
    # -------------------------

    def creer_utilisateur(self, nom_utilisateur: str, mot_de_passe: str) -> Utilisateur:
        if self.utilisateur_dao.verifier_nom_utilisateur_existant(nom_utilisateur):
            raise UtilisateurAlreadyExistsError(
                f"Le nom d'utilisateur '{nom_utilisateur}' existe déjà."
            )

        utilisateur = Utilisateur(
            id=None,
            nom_utilisateur=nom_utilisateur,
        )

        try:
            self.utilisateur_dao.creer(utilisateur, mot_de_passe)
        except DatabaseCreationError:
            raise

        return utilisateur

    # -------------------------
    # Authentification
    # -------------------------

    def authentifier(self, nom_utilisateur: str, mot_de_passe: str) -> Utilisateur:
        try:
            return self.utilisateur_dao.se_connecter(nom_utilisateur, mot_de_passe)
        except (NotFoundError, InvalidPasswordError):
            raise

    # -------------------------
    # Lecture
    # -------------------------

    def lister_utilisateurs(self) -> list[Utilisateur]:
        return self.utilisateur_dao.lister_tous()

    def trouver_par_id(self, id: int) -> Utilisateur:
        utilisateur = self.utilisateur_dao.trouver_par_id(id)
        if utilisateur is None:
            raise NotFoundError("Utilisateur non trouvé.")
        return utilisateur

    # -------------------------
    # Suppression
    # -------------------------

    def supprimer_utilisateur(self, id: int) -> None:
        if not self.utilisateur_dao.verifier_id_existant(id):
            raise NotFoundError("Utilisateur non trouvé.")

        try:
            self.utilisateur_dao.supprimer(id)
        except DatabaseDeletionError:
            raise
