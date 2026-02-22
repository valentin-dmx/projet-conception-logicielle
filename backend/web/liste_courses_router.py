from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.liste_courses_service import ListeCoursesService


router = APIRouter(prefix="/liste-courses", tags=["Panier"])
service = ListeCoursesService()


class IngredientInput(BaseModel):
    nom: str
    quantite: float
    unite: str


class ListeCoursesRequest(BaseModel):
    ingredients: list[IngredientInput]
    activer_prix: bool = True


@router.post("")
def generer_liste_courses(body: ListeCoursesRequest):
    ingredients_dict = [
        {"nom": i.nom, "quantite": i.quantite, "unite": i.unite}
        for i in body.ingredients
    ]

    liste = service.generer_liste_courses(
        ingredients_dict, activer_prix=body.activer_prix
    )

    return {
        "articles": [
            {
                "nom": a.nom,
                "quantite": a.quantite,
                "unite": a.unite,
                "prix_estime": a.prix_estime,
            }
            for a in liste.articles
        ],
        "cout_total_estime": liste.cout_total_estime,
    }
