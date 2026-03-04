import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config.app_config import add_cors_middleware
from web.liste_courses_router import router as liste_courses_router
from web.utilisateur_router import utilisateur_router


app_title = os.getenv("APP_TITLE", "UserAPIEnsai")
app = FastAPI(title=app_title)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige vers la documentation de l'API."""
    return RedirectResponse(url="/docs")


app.include_router(liste_courses_router)
app.include_router(utilisateur_router)

# Configuration CORS
add_cors_middleware(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
