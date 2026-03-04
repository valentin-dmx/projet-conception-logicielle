class Utilisateur:
    def __init__(self, id: int | None, nom_utilisateur: str, role: str = "user"):
        self.id = id
        self.nom_utilisateur = nom_utilisateur
        self.role = role

    def __repr__(self) -> str:
        return f"Utilisateur(id={self.id!r}, nom_utilisateur={self.nom_utilisateur!r})"

    @staticmethod
    def valider_nom_utilisateur(nom_utilisateur: str) -> bool:
        """Valider que le nom d'utilisateur est valide (alphanumérique entre 4 et 16 caractères)"""
        if not (
            len(nom_utilisateur) >= 4
            and len(nom_utilisateur) <= 16
            and nom_utilisateur.isalnum()
        ):
            raise ValueError(
                "Nom d'utilisateur invalide. "
                "Il doit être alphanumérique "
                "et contenir entre 4 et 16 caractères."
            )
        return nom_utilisateur
