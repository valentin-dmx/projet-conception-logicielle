import pytest


class FakePlanning:
    """Objet PlanningRepas simplifié pour les tests."""

    def __init__(self):
        self.id = None
        self.nom = None


class FakePlanningDTO:
    """DTO simulé avec conversion vers PlanningRepas."""

    def __init__(self, planning=None):
        self._planning = planning or FakePlanning()

    def to_planning_repas(self):
        return self._planning


class TestPlanningRepasService:
    """Classe de tests pytest pour PlanningRepasService."""

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        """Initialisation automatique avant chaque test."""
        from backend.services.planning_repas_service import PlanningRepasService

        self.mock_dao = mocker.Mock()
        self.service = PlanningRepasService(self.mock_dao)

    # Création visiteur

    def test_creer_planning_repas_visiteur(self):
        self.mock_dao.creer_planning_repas.return_value = "planning"

        result = self.service.creer_planning_repas_visiteur(7)

        self.mock_dao.creer_planning_repas.assert_called_once_with(7)
        assert result == "planning"

    # Compter plannings utilisateur

    def test_compter_plannings_repas_utilisateur(self):
        self.mock_dao.compter_plannings_repas_utilisateur.return_value = 3

        result = self.service.compter_plannings_repas_utilisateur(1)

        self.mock_dao.compter_plannings_repas_utilisateur.assert_called_once_with(1)
        assert result == 3

    # Création planning utilisateur avec nom

    def test_creer_planning_repas_utilisateur_avec_nom(self):
        fake_planning = FakePlanning()
        fake_dto = FakePlanningDTO(fake_planning)

        self.mock_dao.creer_planning_repas.return_value = fake_dto
        self.mock_dao.compter_plannings_repas_utilisateur.return_value = 2

        result = self.service.creer_planning_repas_utilisateur(
            id_utilisateur=1, nb_jours=5, nom_planning="Mon planning"
        )

        self.mock_dao.creer_planning_repas.assert_called_once_with(5, id_utilisateur=1)

        self.mock_dao.renommer_planning_repas_utilisateur.assert_called_once_with(
            1, 3, "Mon planning"
        )

        assert result.id == 3
        assert result.nom == "Mon planning"

    # Création planning vide utilisateur

    def test_creer_planning_repas_vide_utilisateur(self):
        fake_planning = FakePlanning()
        fake_dto = FakePlanningDTO(fake_planning)

        self.mock_dao.creer_planning_repas.return_value = fake_dto

        result = self.service.creer_planning_repas_vide_utilisateur(1, 4)

        self.mock_dao.creer_planning_repas.assert_called_once_with(
            nb_jours=4, id_utilisateur=1, vide=True
        )

        assert isinstance(result, FakePlanning)

    # Modifier planning

    def test_modifier_planning_repas_utilisateur(self):
        fake_planning = FakePlanning()
        fake_dto = FakePlanningDTO(fake_planning)

        self.mock_dao.modifier_planning_repas_utilisateur.return_value = fake_dto

        result = self.service.modifier_planning_repas_utilisateur(1, 2, 1, "midi", 42)

        self.mock_dao.modifier_planning_repas_utilisateur.assert_called_once_with(
            1, 2, 1, "midi", 42
        )

        assert result is fake_planning

    # Suppression planning

    def test_supprimer_planning_repas_utilisateur(self):
        self.service.supprimer_planning_repas_utilisateur(1, 2)

        self.mock_dao.supprimer_planning_repas_utilisateur.assert_called_once_with(1, 2)

    # Ajouter jour

    def test_ajouter_jour_planning_repas_utilisateur(self):
        fake_planning = FakePlanning()
        fake_dto = FakePlanningDTO(fake_planning)

        self.mock_dao.ajouter_jour_planning_repas_utilisateur.return_value = fake_dto

        result = self.service.ajouter_jour_planning_repas_utilisateur(1, 2)

        self.mock_dao.ajouter_jour_planning_repas_utilisateur.assert_called_once_with(
            1, 2
        )

        assert result is fake_planning

    # Supprimer jour

    def test_supprimer_jour_planning_repas_utilisateur(self):
        fake_planning = FakePlanning()
        fake_dto = FakePlanningDTO(fake_planning)

        self.mock_dao.supprimer_jour_planning_repas_utilisateur.return_value = fake_dto

        result = self.service.supprimer_jour_planning_repas_utilisateur(1, 2)

        self.mock_dao.supprimer_jour_planning_repas_utilisateur.assert_called_once_with(
            1, 2
        )

        assert result is fake_planning

    # Renommer planning

    def test_renommer_planning_repas_utilisateur(self):
        self.service.renommer_planning_repas_utilisateur(1, 2, "Nouveau nom")

        self.mock_dao.renommer_planning_repas_utilisateur.assert_called_once_with(
            1, 2, "Nouveau nom"
        )
