from fastapi import APIRouter
from fastapi.responses import RedirectResponse


systeme_router = APIRouter(tags=["Système"])


@systeme_router.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige vers la documentation de l'API."""
    return RedirectResponse(url="/docs")


@systeme_router.get("/status")
def status():
    return {"status": "OK"}
