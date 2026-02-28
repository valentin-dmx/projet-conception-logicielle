"""
Tests unitaires du service ListeCoursesService.
"""

import pytest

from backend.services.liste_courses_service import ListeCoursesService


@pytest.fixture
def prix_api(mocker):
    """
    Mock du DAO .
    """
    dao = mocker.Mock()
    dao.obtenir_prix.return_value = None
    return dao


@pytest.fixture
def liste_courses_service(prix_api):
    """
    Crée un ListeCoursesService en remplaçant le DAO de prix par un mock.
    """
    service = ListeCoursesService()
    service.prix_api = prix_api
    return service


class TestListeCoursesService:
    """
    Tests unitaires pour ListeCoursesService.
    """

    def test_agregation_ingredients_sans_appel_api(self, liste_courses_service, prix_api):
        """
        Vérifie l'agrégation des ingrédients (ex: "Tomates" + "tomates")
        et l'absence d'appel à l'API quand activer_prix=False.
        """
        ingredients = [
            {"nom": "Tomates", "quantite": 2, "unite": "pièces"},
            {"nom": "tomates", "quantite": 3, "unite": "pièces"},
            {"nom": "pâtes", "quantite": 500, "unite": "g"},
        ]

        resultat = liste_courses_service.generer_liste_courses(ingredients, activer_prix=False)

        tomates = [a for a in resultat.articles if a.nom == "tomates" and a.unite == "pièces"]
        assert len(tomates) == 1
        assert tomates[0].quantite == 5.0

        assert resultat.cout_total_estime is None
        prix_api.obtenir_prix.assert_not_called()

    def test_liste_vide(self, liste_courses_service, prix_api):
        """
        Vérifie qu'une liste vide renvoie une liste de courses vide, sans coût estimé.
        """
        res = liste_courses_service.generer_liste_courses([], activer_prix=False)
        assert res.articles == []
        assert res.cout_total_estime is None
        prix_api.obtenir_prix.assert_not_called()

    def test_detection_ingredients_disponibles(self, liste_courses_service, prix_api):
        """
        Vérifie la soustraction des ingrédients disponibles (inventaire) sur les quantités à acheter.
        """
        ingredients = [
            {"nom": "tomates", "quantite": 5, "unite": "pièces"},
            {"nom": "pates", "quantite": 500, "unite": "g"},
        ]
        disponibles = [
            {"nom": "tomates", "quantite": 2, "unite": "pièces"},
            {"nom": "pates", "quantite": 200, "unite": "g"},
        ]

        resultat = liste_courses_service.generer_liste_courses(
            ingredients, activer_prix=False, disponibles=disponibles
        )

        data = {(a.nom, a.unite): a.quantite for a in resultat.articles}
        assert data[("tomates", "pièces")] == 3.0
        assert data[("pates", "g")] == 300.0
        assert resultat.cout_total_estime is None
        prix_api.obtenir_prix.assert_not_called()

    @pytest.mark.parametrize(
        "ingredients, attendu",
        [
            (
                [
                    {"nom": "sucre", "quantite": 500, "unite": "g"},
                    {"nom": "Sucre", "quantite": 1, "unite": "kg"},
                ],
                {("sucre", "g"): 500.0, ("sucre", "kg"): 1.0},
            ),
        ],
    )
    def test_pas_agregation_si_unite_differente(self, liste_courses_service, prix_api, ingredients, attendu):
        """
        Vérifie que deux ingrédients de même nom mais unités différentes ne sont pas agrégés.
        """
        resultat = liste_courses_service.generer_liste_courses(ingredients, activer_prix=False)
        data = {(a.nom, a.unite): a.quantite for a in resultat.articles}
        assert data == attendu
        prix_api.obtenir_prix.assert_not_called()

    def test_estimation_prix_total_et_prix_par_article(self, liste_courses_service, prix_api):
        """
        Vérifie que si activer_prix=True :
        - chaque article reçoit un prix_estime si le prix est trouvé
        - cout_total_estime correspond à la somme des prix
        - l'API est appelée une fois par article agrégé.
        """
        def fake_prix(nom: str):
            mapping = {"tomates": (7.5, "EUR"), "pates": (4.0, "EUR")}
            return mapping.get(nom)

        prix_api.obtenir_prix.side_effect = fake_prix

        ingredients = [
            {"nom": "Tomates", "quantite": 2, "unite": "pièces"},
            {"nom": "tomates", "quantite": 3, "unite": "pièces"},
            {"nom": "pates", "quantite": 500, "unite": "g"},
        ]

        resultat = liste_courses_service.generer_liste_courses(ingredients, activer_prix=True)

        assert resultat.cout_total_estime == 11.5
        data_prix = {a.nom: getattr(a, "prix_estime", None) for a in resultat.articles}
        assert data_prix["tomates"] == 7.5
        assert data_prix["pates"] == 4.0

        assert prix_api.obtenir_prix.call_count == 2

    def test_prix_introuvable_ignore_du_total(self, liste_courses_service, prix_api):
        """
        Vérifie que si un article n'a pas de prix (None), il est ignoré dans le total estimé.
        """
        def fake_prix(nom: str):
            if nom == "tomates":
                return (3.0, "EUR")
            return None

        prix_api.obtenir_prix.side_effect = fake_prix

        ingredients = [
            {"nom": "tomates", "quantite": 5, "unite": "pièces"},
            {"nom": "pates", "quantite": 500, "unite": "g"},
        ]

        resultat = liste_courses_service.generer_liste_courses(ingredients, activer_prix=True)

        assert resultat.cout_total_estime == 3.0
        data_prix = {a.nom: getattr(a, "prix_estime", None) for a in resultat.articles}
        assert data_prix["tomates"] == 3.0
        assert data_prix["pates"] is None

    def test_inventaire_superieur_au_besoin_pas_de_negatif(self, liste_courses_service, prix_api):
        """
        Vérifie que si l'inventaire contient plus que le besoin, la quantité à acheter n'est pas négative
        (0 ou suppression de l'article selon le comportement du BO).
        """
        ingredients = [{"nom": "tomates", "quantite": 2, "unite": "pièces"}]
        disponibles = [{"nom": "tomates", "quantite": 10, "unite": "pièces"}]

        resultat = liste_courses_service.generer_liste_courses(
            ingredients, activer_prix=False, disponibles=disponibles
        )

        data = {(a.nom, a.unite): a.quantite for a in resultat.articles}
        if ("tomates", "pièces") in data:
            assert data[("tomates", "pièces")] == 0.0

        prix_api.obtenir_prix.assert_not_called()

    @pytest.mark.parametrize("disponibles", [None, []])
    def test_disponibles_vide_equivaut_aucun_inventaire(self, liste_courses_service, prix_api, disponibles):
        """
        Vérifie que disponibles=None et disponibles=[] donnent le même résultat
        (dans le service, `if disponibles:` traite [] comme False).
        """
        ingredients = [
            {"nom": "tomates", "quantite": 5, "unite": "pièces"},
            {"nom": "pates", "quantite": 500, "unite": "g"},
        ]

        resultat = liste_courses_service.generer_liste_courses(
            ingredients, activer_prix=False, disponibles=disponibles
        )

        data = {(a.nom, a.unite): a.quantite for a in resultat.articles}
        assert data[("tomates", "pièces")] == 5.0
        assert data[("pates", "g")] == 500.0
        assert resultat.cout_total_estime is None
        prix_api.obtenir_prix.assert_not_called()
