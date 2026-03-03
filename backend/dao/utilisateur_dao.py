from business_object.utilisateur import Utilisateur
from dao.configuration.db_connection import DBConnection
from dao.exceptions import (
    DatabaseCreationError,
    DatabaseDeletionError,
    InvalidPasswordError,
    NotFoundError,
)
from utils.securite import generer_salt, hash_password, verifier_mot_de_passe


class UtilisateurDao:
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base de données"""

    def creer(self, utilisateur: Utilisateur, mot_de_passe: str) -> bool:
        """Création d'un utilisateur et de ses credentials associés dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            L'objet Utilisateur contenant les informations personnelles à insérer
        mot_de_passe : str
            Le mot de passe en clair qui sera hashé et stocké dans les credentials

        Returns
        -------
        bool
            True si l'utilisateur et ses credentials ont été créés avec succès
        """
        # Générer un sel et le hash correspondant
        sel = generer_salt()
        mot_de_passe_hash = hash_password(mot_de_passe, sel)

        with DBConnection().connection as connection, connection.cursor() as cursor:
            # Étape 1 : création de l'utilisateur (id auto-généré)
            cursor.execute(
                """
                INSERT INTO utilisateur (nom_utilisateur)
                VALUES (%(nom_utilisateur)s)
                RETURNING id;
                """,
                {
                    "nom_utilisateur": utilisateur.nom_utilisateur,
                },
            )
            res = cursor.fetchone()
            if res is None:
                raise DatabaseCreationError("Echec de la création de l'utilisateur.")

            # Récupération de l'id auto-généré
            utilisateur.id = res["id"]

            # Étape 2 : insérer les credentials
            cursor.execute(
                """
                INSERT INTO credentials (id, mot_de_passe_hash, sel)
                VALUES (%(id)s, %(mot_de_passe_hash)s, %(sel)s);
                """,
                {
                    "id": utilisateur.id,
                    "mot_de_passe_hash": mot_de_passe_hash,
                    "sel": sel,
                },
            )
        # Si on arrive ici, commit du bloc, sinon, rollback automatique
        # (donc l'utilisateur et les credentials sont forcément créés ensemble)

        return True

    def trouver_par_nom_utilisateur(self, nom_utilisateur: str) -> Utilisateur | None:
        """Trouver un utilisateur grâce à son nom d'utilisateur

        Parameters
        ----------
        nom_utilisateur : str
            Nom de l'utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche par nom d'utilisateur
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM utilisateur WHERE nom_utilisateur = %(nom_utilisateur)s;",
                {"nom_utilisateur": nom_utilisateur},
            )
            res = cursor.fetchone()

        if res:
            utilisateur = Utilisateur(
                id=res["id"],
                nom_utilisateur=res["nom_utilisateur"],
            )
            return utilisateur
        return None

    def trouver_par_id(self, id: int) -> Utilisateur | None:
        """Trouver un utilisateur par son identifiant

        Parameters
        ----------
        id : int
            L'identifiant de l'utilisateur recherché

        Returns
        -------
        Utilisateur | None
            L'objet Utilisateur correspondant si trouvé, sinon None
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM utilisateur WHERE id = %(id)s;",
                {"id": id},
            )
            res = cursor.fetchone()

        if res:
            utilisateur = Utilisateur(
                id=res["id"],
                nom_utilisateur=res["nom_utilisateur"],
            )
            return utilisateur
        return None

    def lister_tous(self) -> list[Utilisateur]:
        """Lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        List[Utilisateur]
            Renvoie la liste de tous les utilisateurs dans la base de données
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM utilisateur;")
            res = cursor.fetchall()

        liste_utilisateurs = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id=row["id"],
                    nom_utilisateur=row["nom_utilisateur"],
                )
                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    def supprimer(self, id: int) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        id : int
            l'id de l'utilisateur à supprimer de la base de données

        Returns
        -------
        True si l'utilisateur a bien été supprimé
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM utilisateur WHERE id = %(id)s;",
                {"id": id},
            )
            res = cursor.rowcount

        if res < 1:
            msg_err = (
                "Echec de la suppression de l'utilisateur : "
                "aucune ligne retournée par la base"
            )
            raise DatabaseDeletionError(msg_err)

        return True

    def verifier_nom_utilisateur_existant(self, nom_utilisateur: str) -> bool:
        """Vérifier si un nom d'utilisateur est déjà utilisé dans la base de données

        Parameters
        ----------
        nom_utilisateur : str
            Le nom d'utilisateur dont on veut vérifier l'existence

        Returns
        -------
        bool
            True si le nom d'utilisateur existe déjà, False sinon
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM utilisateur WHERE nom_utilisateur = %(nom_utilisateur)s;",
                {"nom_utilisateur": nom_utilisateur},
            )
            res = cursor.fetchone()
            return (
                res is not None
            )  # Si un résultat est trouvé, le nom d'utilisateur existe déjà

    def verifier_id_existant(self, id: int) -> bool:
        """Vérifier si un utilisateur existe via son identifiant

        Parameters
        ----------
        id : int
            Identifiant de l'utilisateur à vérifier

        Returns
        -------
        bool
            True si l'utilisateur existe, False sinon
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM utilisateur WHERE id = %(id)s;",
                {"id": id},
            )
            res = cursor.fetchone()
            return res is not None

    def se_connecter(
        self, nom_utilisateur: str, mot_de_passe: str
    ) -> Utilisateur | None:
        """Authentification d'un utilisateur via nom d'utilisateur et mot de passe

        Parameters
        ----------
        nom_utilisateur : str
            Le nom de l'utilisateur tentant de se connecter
        mot_de_passe : str
            Le mot de passe fourni lors de la connexion

        Returns
        -------
        Utilisateur | None
            L'objet Utilisateur correspondant si l'authentification réussit.
            None n'est jamais retourné car une exception est levée en cas d'échec.
        """
        with DBConnection().connection as connection, connection.cursor() as cursor:
            # Récupérer l'utilisateur et son mot de passe haché via jointure
            cursor.execute(
                """
                SELECT u.id, u.nom_utilisateur,
                    c.mot_de_passe_hash, c.sel
                FROM utilisateur u
                JOIN credentials c ON u.id = c.id
                WHERE u.nom_utilisateur = %(nom_utilisateur)s;
                """,
                {"nom_utilisateur": nom_utilisateur},
            )
            res = cursor.fetchone()

        if res is None:
            msg_err = (
                f"Aucun utilisateur trouvé avec le nom d'utilisateur {nom_utilisateur}"
            )
            raise NotFoundError(msg_err)

        # Vérification du mot de passe
        if not verifier_mot_de_passe(
            mot_de_passe, res["sel"], res["mot_de_passe_hash"]
        ):
            msg_err = f"Mot de passe incorrect pour {nom_utilisateur}"
            raise InvalidPasswordError(msg_err)

        # Création de l'objet métier Utilisateur
        utilisateur = Utilisateur(
            id=res["id"],
            nom_utilisateur=res["nom_utilisateur"],
        )

        return utilisateur
