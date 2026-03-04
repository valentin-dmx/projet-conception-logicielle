from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Autorise toutes les origines
        allow_credentials=True,
        allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
        allow_headers=["*"],  # Autorise tous les headers
    )
