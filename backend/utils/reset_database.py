import os

import dotenv

from dao.configuration.db_connection import DBConnection
from utils.securite import generer_salt, hash_password
from utils.singleton import Singleton


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données
    """

    def lancer(self):
        """Lancement de la réinitialisation des données"""
        pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = (
            f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"
        )

        with open("data/init_db.sql", encoding="utf-8") as init_db:
            init_db_as_string = init_db.read()

        with open(pop_data_path, encoding="utf-8") as pop_db:
            pop_db_as_string = pop_db.read()

        with DBConnection().connection as connection, connection.cursor() as cursor:
            cursor.execute(create_schema)
            cursor.execute(init_db_as_string)
            cursor.execute(pop_db_as_string)

            # Récupérer tous les credentials et remplacer les mots de passe bruts
            cursor.execute("SELECT id, mot_de_passe_hash FROM credentials;")
            credentials = cursor.fetchall()

            for cred in credentials:
                # mot_de_passe_hash contient temporairement le mot de passe en clair (ex: "mdp1")
                mot_de_passe_clair = cred["mot_de_passe_hash"]
                sel = generer_salt()
                mot_de_passe_hash = hash_password(mot_de_passe_clair, sel)

                cursor.execute(
                    """
                    UPDATE credentials
                    SET mot_de_passe_hash = %(hash)s, sel = %(sel)s
                    WHERE id = %(id)s;
                    """,
                    {
                        "hash": mot_de_passe_hash,
                        "sel": sel,
                        "id": cred["id"],
                    },
                )

        print("Succès de la réinitialisation de la base de données")
        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
