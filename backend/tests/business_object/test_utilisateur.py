import pytest

from business_object.utilisateur import Utilisateur


def test_validation_ok():
    assert Utilisateur.valider_nom_utilisateur("john") == "john"


def test_validation_ko():
    with pytest.raises(ValueError):
        Utilisateur.valider_nom_utilisateur("a")
