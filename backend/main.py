import os

from fastapi import FastAPI

from config.app_config import add_cors_middleware
from web.liste_courses_router import router as liste_courses_router
from web.systeme_router import systeme_router
from web.utilisateur_router import utilisateur_router


app_title = os.getenv("APP_TITLE", "NutriPlan")
app = FastAPI(title=app_title)

app.include_router(systeme_router)
app.include_router(liste_courses_router)
app.include_router(utilisateur_router)

# Configuration CORS
add_cors_middleware(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
