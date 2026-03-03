class DatabaseCreationError(Exception):
    """Levé lors de l'échec d'une création dans la base de données"""

    pass


class DatabaseDeletionError(Exception):
    """Levé lors de l'échec d'une suppression dans la base de données"""

    pass


class NotFoundError(Exception):
    """Levé lorsqu'une ressource demandée n'existe pas"""

    pass


class InvalidPasswordError(Exception):
    """Levé lorsque le mot de passe ne correspond pas à un utilisateur"""

    pass
