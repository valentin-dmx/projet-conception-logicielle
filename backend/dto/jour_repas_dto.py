from business_object.jour_repas import JourRepas


class JourRepasDTO:
    """
    DTO représentant les repas d'un jour.
    """

    def __init__(
        self,
        numero_jour: int,
        petit_dejeuner: int | None = None,
        dejeuner: int | None = None,
        diner: int | None = None,
    ):
        self.numero_jour = numero_jour
        self.petit_dejeuner = petit_dejeuner
        self.dejeuner = dejeuner
        self.diner = diner

    @staticmethod
    def bo_to_dto(jour_bo):
        if jour_bo is None:
            return None

        return JourRepasDTO(
            numero_jour=jour_bo.numero_jour,
            petit_dejeuner=jour_bo.petit_dejeuner,
            dejeuner=jour_bo.dejeuner,
            diner=jour_bo.diner,
        )

    @staticmethod
    def dto_to_bo(self):
        return JourRepas(
            numero_jour=self.numero_jour,
            petit_dejeuner=self.petit_dejeuner,
            dejeuner=self.dejeuner,
            diner=self.diner,
        )
