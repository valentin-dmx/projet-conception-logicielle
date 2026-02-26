from backend.services.liste_courses_service import ListeCoursesService


def test_agregation_ingredients_sans_appel_api():
    service = ListeCoursesService()

    ingredients = [
        {"nom": "Tomates", "quantite": 2, "unite": "pièces"},
        {"nom": "tomates", "quantite": 3, "unite": "pièces"},
        {"nom": "pâtes", "quantite": 500, "unite": "g"},
    ]

    resultat = service.generer_liste_courses(ingredients, activer_prix=False)

    # tomates doivent être regroupées: 2 + 3 = 5
    tomates = [
        a for a in resultat.articles if a.nom == "tomates" and a.unite == "pièces"
    ]
    assert len(tomates) == 1
    assert tomates[0].quantite == 5.0

    # pas d'appel API donc pas de total estimé
    assert resultat.cout_total_estime is None


def test_liste_vide():
    service = ListeCoursesService()
    res = service.generer_liste_courses([], activer_prix=False)
    assert res.articles == []


def test_detection_ingredients_disponibles():
    service = ListeCoursesService()

    ingredients = [
        {"nom": "tomates", "quantite": 5, "unite": "pièces"},
        {"nom": "pates", "quantite": 500, "unite": "g"},
    ]

    disponibles = [
        {"nom": "tomates", "quantite": 2, "unite": "pièces"},
        {"nom": "pates", "quantite": 200, "unite": "g"},
    ]

    resultat = service.generer_liste_courses(
        ingredients,
        activer_prix=False,
        disponibles=disponibles,
    )

    data = {(a.nom, a.unite): a.quantite for a in resultat.articles}
    assert data[("tomates", "pièces")] == 3.0
    assert data[("pates", "g")] == 300.0
    assert resultat.cout_total_estime is None
