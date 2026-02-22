from fastapi import FastAPI

from backend.web.liste_courses_router import router as liste_courses_router

app = FastAPI()
app.include_router(liste_courses_router)


@app.get("/health")
def health():
    return {"status": "ok"}