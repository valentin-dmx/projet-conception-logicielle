import pytest

from backend.services.planning_repas_service import PlanningRepasService


# ------------------------------------------------------------------
# Fake objets cohérents avec le fonctionnement Spoonacular (DTO)
# ------------------------------------------------------------------


class FakePlanning:
    def __init__(self, id=None, nom=None, nb_jours=0):
        self.id = id
        self.nom = nom
        self.nb_jours = nb_jours


class FakePlanningDTO:
    def __init__(self, planning):
        self._planning = planning

    def to_planning_repas(self):
        return self._planning


# ==================================================================
#                       CLASSE DE TEST PYTEST
# ==================================================================


class TestPlanningRepasService:
    @pytest.fixture
    def dao_mock(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def service(self, dao_mock):
        return PlanningRepasService(dao_mock)

    # --------------------------------------------------------------
    # CREATION VISITEUR
    # --------------------------------------------------------------

    def test_creer_planning_repas_visiteur(self, service, dao_mock):
        fake_planning = FakePlanning(nb_jours=3)
        dao_mock.creer_planning_repas.return_value = fake_planning

        result = service.creer_planning_repas_visiteur(3)

        dao_mock.creer_planning_repas.assert_called_once_with(3)
        assert result.nb_jours == 3

    # --------------------------------------------------------------
    # COMPTER
    # --------------------------------------------------------------

    def test_compter_plannings_repas_utilisateur(self, service, dao_mock):
        dao_mock.compter_plannings_repas_utilisateur.return_value = 4

        result = service.compter_plannings_repas_utilisateur(10)

        dao_mock.compter_plannings_repas_utilisateur.assert_called_once_with(10)
        assert result == 4

    # --------------------------------------------------------------
    # CREATION UTILISATEUR AVEC NOM
    # --------------------------------------------------------------

    def test_creer_planning_repas_utilisateur_avec_nom(self, service, dao_mock):
        fake_planning = FakePlanning(nb_jours=7)
        fake_dto = FakePlanningDTO(fake_planning)

        dao_mock.creer_planning_repas.return_value = fake_dto
        dao_mock.compter_plannings_repas_utilisateur.return_value = 2

        result = service.creer_planning_repas_utilisateur(
            id_utilisateur=1, nb_jours=7, nom_planning="Planning semaine"
        )

        # ID = compteur + 1
        assert result.id == 3
        assert result.nom == "Planning semaine"

        dao_mock.renommer_planning_repas_utilisateur.assert_called_once_with(
            1, 3, "Planning semaine"
        )

    # --------------------------------------------------------------
    # CREATION UTILISATEUR SANS NOM
    # --------------------------------------------------------------

    def test_creer_planning_repas_utilisateur_sans_nom(self, service, dao_mock):
        fake_planning = FakePlanning(nb_jours=5)
        fake_dto = FakePlanningDTO(fake_planning)

        dao_mock.creer_planning_repas.return_value = fake_dto
        dao_mock.compter_plannings_repas_utilisateur.return_value = 0

        result = service.creer_planning_repas_utilisateur(id_utilisateur=1, nb_jours=5)

        assert result.id == 1
        dao_mock.renommer_planning_repas_utilisateur.assert_not_called()

    # --------------------------------------------------------------
    # MODIFIER
    # --------------------------------------------------------------

    def test_modifier_planning_repas_utilisateur(self, service, dao_mock):
        fake_planning = FakePlanning(id=1)
        fake_dto = FakePlanningDTO(fake_planning)

        dao_mock.modifier_planning_repas_utilisateur.return_value = fake_dto

        result = service.modifier_planning_repas_utilisateur(
            id_utilisateur=1,
            planning_id=1,
            jour_modif=2,
            moment_modif="midi",
            id_plat_modif=123,
        )

        dao_mock.modifier_planning_repas_utilisateur.assert_called_once_with(
            1, 1, 2, "midi", 123
        )

        assert result.id == 1

    # --------------------------------------------------------------
    # SUPPRIMER
    # --------------------------------------------------------------

    def test_supprimer_planning_repas_utilisateur(self, service, dao_mock):
        service.supprimer_planning_repas_utilisateur(1, 2)

        dao_mock.supprimer_planning_repas_utilisateur.assert_called_once_with(1, 2)

    # --------------------------------------------------------------
    # AJOUT JOUR
    # --------------------------------------------------------------

    def test_ajouter_jour_planning(self, service, dao_mock):
        fake_planning = FakePlanning(nb_jours=4)
        fake_dto = FakePlanningDTO(fake_planning)

        dao_mock.ajouter_jour_planning_repas_utilisateur.return_value = fake_dto

        result = service.ajouter_jour_planning_repas_utilisateur(1, 1)

        assert result.nb_jours == 4

    # --------------------------------------------------------------
    # SUPPRESSION JOUR
    # --------------------------------------------------------------

    def test_supprimer_jour_planning(self, service, dao_mock):
        fake_planning = FakePlanning(nb_jours=2)
        fake_dto = FakePlanningDTO(fake_planning)

        dao_mock.supprimer_jour_planning_repas_utilisateur.return_value = fake_dto

        result = service.supprimer_jour_planning_repas_utilisateur(1, 1)

        assert result.nb_jours == 2

    # --------------------------------------------------------------
    # RENOMMER
    # --------------------------------------------------------------

    def test_renommer_planning(self, service, dao_mock):
        service.renommer_planning_repas_utilisateur(1, 1, "Nouveau nom")

        dao_mock.renommer_planning_repas_utilisateur.assert_called_once_with(
            1, 1, "Nouveau nom"
        )
