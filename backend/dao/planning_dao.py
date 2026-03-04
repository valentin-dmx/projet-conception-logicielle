import logging

from dao.db_connection import DBConnection

from backend.business_object.planning_repas import PlanningRepas


MOMENTS = ["petit_dejeuner", "dejeuner", "diner"]


class PlanningDAO:
    """
    Classe de base pour les DAO de planning.
    """

    def __init__(self):
        pass

    def ajouter_planning_repas_utilisateur(
        self, planning_repas: PlanningRepas
    ) -> PlanningRepas:
        """
        Ajoute un nouveau planning de repas pour un utilisateur.

        Params
        ----------
            planning_repas: PlanningRepas
                Un objet représentant le planning de repas à ajouter pour l'utilisateur.
        Return
        ----------
            PlanningRepas
                Le planning de repas ajouté pour l'utilisateur.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                # Insertion du planning
                cursor.execute(
                    """
                        INSERT INTO planning_repas(id_user, nom_planning)
                        VALUES (%s, %s)
                        RETURNING id_planning;
                        """,
                    (planning_repas.id_utilisateur, planning_repas.nom),
                )

                id_planning = cursor.fetchone()[0]

                # Insertion des repas
                for jour in planning_repas.jours:
                    for moment, id_plat in jour.to_dict().items():
                        cursor.execute(
                            """
                                INSERT INTO jour_planning_repas
                                (id_planning, jour, moment_journee, id_plat)
                                VALUES (%s, %s, %s, %s);
                                """,
                            (id_planning, jour.numero_jour, moment, id_plat),
                        )

        except Exception as e:
            logging.info(e)
            raise

        return self.voir_planning_repas(planning_repas.id_utilisateur, id_planning)

    def compter_planning_repas_utilisateur(self, id_utilisateur: int) -> int:
        """
        Compte le nombre de plannings de repas associés à un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur dont on veut compter les plannings de repas.
        Return
        ----------
            int
                Le nombre de plannings de repas associés à l'utilisateur fourni.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """SELECT COUNT(*) FROM planning_repas WHERE id_user = %(id_utilisateur)s;""",
                    {"id_utilisateur": id_utilisateur},
                )
                res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
            raise

        return res[0] if res else 0

    def voir_planning_repas(
        self, id_utilisateur: int, id_planning: int
    ) -> PlanningRepas:
        """
        Récupère un planning de repas par son ID.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à récupérer.
        Return
        ----------
            PlanningRepas
                Le PlanningRepas représentant le planning de repas correspondant à l'ID fourni.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT pr.id_planning,
                        pr.nom_planning,
                        jpr.jour,
                            jpr.moment_journee,
                            jpr.id_plat
                        FROM planning_repas pr
                        JOIN jour_planning_repas jpr
                            ON pr.id_planning = jpr.id_planning
                        WHERE pr.id_user = %(id_utilisateur)s
                        AND pr.id_planning = %(id_planning)s
                        ORDER BY jpr.jour;
                        """,
                    {"id_utilisateur": id_utilisateur, "id_planning": id_planning},
                )

                rows = cursor.fetchall()

        except Exception as e:
            logging.info(e)
            raise

        if not rows:
            raise ValueError("Planning non trouvé.")

        planning = PlanningRepas(
            id_utilisateur=id_utilisateur,
            id=rows[0][0],  # id_planning
            nom=rows[0][1],  # nom_planning
            nb_jours=max(row[2] for row in rows),
        )

        for row in rows:
            jour_num = row[2]
            moment = row[3]
            id_plat = row[4]

            jour = planning.jours[jour_num - 1]

            if moment == "petit_dejeuner":
                jour.petit_dejeuner = id_plat
            elif moment == "dejeuner":
                jour.dejeuner = id_plat
            elif moment == "diner":
                jour.diner = id_plat

        return planning

    def voir_tous_planning_repas_utilisateur(
        self, id_utilisateur: int
    ) -> list[PlanningRepas]:
        """
        Récupère tous les plannings de repas associés à un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur dont on veut récupérer les plannings de repas.
        Return
        ----------
            list[PlanningRepas]
                Une liste de PlpanningRepas représentant tous les plannings de repas associés à l'utilisateur fourni.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT DISTINCT id_planning
                    FROM planning_repas
                    WHERE id_user = %(id_utilisateur)s;
                        """,
                    {"id_utilisateur": id_utilisateur},
                )
                rows = cursor.fetchall()

        except Exception as e:
            logging.info(e)
            raise

        plannings = [self.voir_planning_repas(id_utilisateur, row[0]) for row in rows]

        return plannings

    def renommer_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int, nouveau_nom: str
    ) -> PlanningRepas:
        """
        Renomme un planning de repas pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à renommer.
            nouveau_nom: str
                Le nouveau nom à attribuer au planning de repas.
        Return
        ----------
            PlanningRepas
                Le planning de repas renommé pour l'utilisateur.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE planning_repas SET nom_planning = %(nouveau_nom)s
                        WHERE id_user = %(id_utilisateur)s AND id_planning = %(id_planning)s;""",
                    {
                        "nouveau_nom": nouveau_nom,
                        "id_utilisateur": id_utilisateur,
                        "id_planning": id_planning,
                    },
                )
        except Exception as e:
            logging.info(e)
            raise
        return self.voir_planning_repas(id_utilisateur, id_planning)

    def supprimer_planning_repas_utilisateur(
        self, id_utilisateur: int, id_planning: int
    ) -> None:
        """
        Supprime un planning de repas pour un utilisateur.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à supprimer.
        Return
        ----------
            None
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                # Supprimer d'abord les jours
                cursor.execute(
                    """
                    DELETE FROM jour_planning_repas
                    WHERE id_planning = %(id_planning)s;
                        """,
                    {"id_planning": id_planning},
                )

                # Puis supprimer le planning
                cursor.execute(
                    """
                    DELETE FROM planning_repas
                    WHERE id_user = %(id_utilisateur)s
                    AND id_planning = %(id_planning)s;
                    """,
                    {"id_utilisateur": id_utilisateur, "id_planning": id_planning},
                )

                if cursor.rowcount == 0:
                    raise ValueError("Planning non trouvé ou non supprimé.")

        except Exception as e:
            logging.info(e)
            raise

    def modifier_planning_repas_utilisateur(
        self,
        id_utilisateur: int,
        id_planning: int,
        jour_modif: int,
        moment_modif: str,
        id_plat_modif: int,
    ) -> PlanningRepas:
        """
        Modifie un planning de repas existant pour un utilisateur avec les nouvelles informations fournies dans le PlanningRepas.

        Params
        ----------
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
            planning_id: int
                L'ID du planning de repas à modifier.
            jour_modif: int
                Le jour du planning de repas à modifier.
            moment_modif: str
                Le moment du jour à modifier (ex: "petit_dejeuner", "dejeuner", "diner").
            id_plat_modif: int
                L'ID du plat à associer au jour et moment modifiés du planning de repas.
        Return
        ----------
            PlanningRepas
                Un PlanningRepas représentant le planning de repas modifié pour l'utilisateur.
        """

        if moment_modif not in MOMENTS:
            raise ValueError("Moment invalide.")
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE jour_planning_repas
                    SET id_plat = %(id_plat_modif)s
                    WHERE id_planning = %(id_planning)s
                        AND jour = %(jour_modif)s
                        AND moment_journee = %(moment_modif)s
                        RETURNING id_planning;
                        """,
                    {
                        "id_plat_modif": id_plat_modif,
                        "id_planning": id_planning,
                        "jour_modif": jour_modif,
                        "moment_modif": moment_modif,
                    },
                )

                if cursor.fetchone() is None:
                    raise ValueError("Modification impossible.")

        except Exception as e:
            logging.info(e)
            raise

        return self.voir_planning_repas(id_utilisateur, id_planning)

    def ajouter_jour_planning_repas_utilisateur(
        self, id_planning: int, id_utilisateur: int
    ) -> PlanningRepas:
        """
        Ajoute un jour à un planning de repas.

        Params
        ----------
            id_planning: int
                L'ID du planning de repas auquel ajouter un jour.
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
        Return
        ----------
            PlanningRepas
                Le planning de repas mis à jour pour l'utilisateur.
        """
        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                # Récupérer le prochain numéro de jour
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(jour), 0) + 1
                    FROM jour_planning_repas
                        WHERE id_planning = %(id_planning)s;
                        """,
                    {"id_planning": id_planning},
                )
                new_jour = cursor.fetchone()[0]

                # Insérer les 3 moments avec NULL
                for moment in MOMENTS:
                    cursor.execute(
                        """
                        INSERT INTO jour_planning_repas
                        (id_planning, jour, moment_journee, id_plat)
                        VALUES (%(id_planning)s, %(jour)s, %(moment)s, NULL);
                        """,
                        {
                            "id_planning": id_planning,
                            "jour": new_jour,
                            "moment": moment,
                        },
                    )

        except Exception as e:
            logging.info(e)
            raise

        return self.voir_planning_repas(id_utilisateur, id_planning)

    def supprimer_jour_planning_repas_utilisateur(
        self, id_planning: int, id_utilisateur: int
    ) -> PlanningRepas:
        """
        Supprime un jour d'un planning de repas.

        Params
        ----------
            id_planning: int
                L'ID du planning de repas auquel supprimer un jour.
            id_utilisateur: int
                L'ID de l'utilisateur auquel le planning de repas est associé.
        Return
        ----------
            PlanningRepas
                Le planning de repas mis à jour pour l'utilisateur.
        """
        planning = self.voir_planning_repas(id_utilisateur, id_planning)
        if planning.nb_jours <= 1:
            raise ValueError("Impossible de supprimer le dernier jour.")

        try:
            with DBConnection().connection as connection, connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM jour_planning_repas
                        WHERE id_planning = %(id_planning)s
                        AND jour = (SELECT MAX(jour) FROM jour_planning_repas WHERE id_planning = %(id_planning)s);""",
                    {"id_planning": id_planning},
                )
        except Exception as e:
            logging.info(e)
            raise
        return self.voir_planning_repas(id_utilisateur, id_planning)
