import pytest

from business_object.ingredient import Ingredient
from business_object.plat import Plat
from services.plat_service import PlatService


@pytest.fixture
def dao(mocker):
    dao = mocker.Mock()
    dao.recherche_plat_nom.return_value = [mocker.Mock(id=1, nom="Lasagnes")]
    dao.information_plat.return_value = mocker.Mock(id=2, nom="Pizza")
    dao.get_plat_ingredients.return_value = [
        mocker.Mock(id=10, nom="Tomate", quantite=2, unite="pcs")
    ]
    return dao


@pytest.fixture
def plat_service(dao):
    return PlatService(dao=dao)


class TestPlatService:
    """
    Tests unitaires pour le service de gestion des plats.
    """

    def test_rechercher_plat_nom(self, plat_service, dao):
        resultat = plat_service.rechercher_plat_nom("lasagnes")

        assert len(resultat) == 1
        assert isinstance(resultat[0], Plat)
        assert resultat[0].nom == "Lasagnes"
        dao.recherche_plat_nom.assert_called_once_with("lasagnes")

    def test_information_plat(self, plat_service, dao):
        resultat = plat_service.information_plat(2)
        assert isinstance(resultat, Plat)
        assert resultat.id == 2
        dao.information_plat.assert_called_once_with(2)

    def test_plat_ingredients(self, plat_service, dao):
        resultat = plat_service.plat_ingredients(99)
        assert len(resultat) == 1
        assert isinstance(resultat[0], Ingredient)
        assert str.lower(resultat[0].nom) == "tomate"
        dao.get_plat_ingredients.assert_called_once_with(99)
