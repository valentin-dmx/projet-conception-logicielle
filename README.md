# projet-conception-logicielle

## :arrow\_forward: Présentation

Cette application permet de chercher des recettes de cuisine, de planifier ses repas et de générer une liste de courses, le tout avec un système utilisateur. Il s'agit d'une application backend exposant une API REST.

## :arrow\_forward: Architecture du code

## Backend (./backend)

L'application met en œuvre :
- Git avec utilisation de branches et merge requests
- Architecture applicative (couches, IoC, SRP)
- Linting et qualité du code (avec pipeline automatisée)
- Tests unitaires utilisant Pytest (avec pipeline automatisée)
- CI/CD
- Design patterns et bonnes pratiques
- Portabilité avec Docker, Kubernetes
- Authentification sécurisée
- Utilisation des API Spoonacular et Open Food Facts
- Documentation (dépendances, quickstart, utilisation...)

L'application suit une architecture en couches claire :
Router (web/)
   ↓
Service (services/)
   ↓
DAO (dao/)
   ↓
Base de données

## Aperçu des fichiers backend

| Fichier / Dossier  | Description                                                                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`          | **Point d'entrée de l'API FastAPI**. Initialise l'application, enregistre les routeurs et configure les middlewares (CORS, etc.).                  |
| `business_object/` | Contient les **objets métier** (ex : `Utilisateur`). Représentation purement métier des entités, indépendante de FastAPI et de la base de données. |
| `web/`             | Contient les **routeurs FastAPI** (ex : `utilisateur_router.py`). Définit les endpoints HTTP et la gestion des réponses.                           |
| `services/`        | Couche **logique métier**. Intermédiaire entre les routeurs et les DAO. Gère les règles métier (authentification, rôles, permissions…).            |
| `dao/`             | Couche **accès aux données**. Contient les classes responsables des requêtes SQL et des interactions avec la base de données.                      |
| `dto/`             | Contient les **Data Transfer Objects** (Pydantic). Définit les modèles utilisés pour les requêtes et réponses API.                                 |
| `config/`          | Configuration technique de l'application (ex : CORS Middleware, paramètres globaux).                                                               |
| `utils/`           | Fonctions utilitaires transverses (ex : `securite` pour hash/salt des mots de passe, `reset_database`).                                            |
| `data/`            | Scripts SQL d'initialisation et de structure de la base de données.                                                                                |
| `tests/`           | Tests unitaires et/ou d'intégration (DAO, services, routes…).                                                                                      |
| `.env.template`    | Modèle de fichier d'environnement (variables de configuration : BDD, ports…).                                                                      |
| `pyproject.toml`   | Configuration du projet Python (dépendances, outils, build).                                                                                       |
| `uv.lock`          | Fichier de verrouillage des dépendances (gestion via `uv`).                                                                                        |
| `ruff.toml`        | Configuration du linter **Ruff**.                                                                                                                  |
| `Dockerfile`       | Fichier de conteneurisation pour déployer l'application dans Docker.                                                                               |
| `.python-version`  | Version Python utilisée par le projet (pyenv ou équivalent).                                                                                       |


## Déploiement Cloud (./kubernetes)
Contient les scripts Kubernetes nécessaires au déploiement de l’application.

## :arrow\_forward: Quickstart pour un lancement avec VSCode

## Prérequis

Vous devez avoir installé uv.

Clonez le dépôt ici présent.

Créez une base de données PostgreSQL (par exemple à l'aide d'un Datalab).

## Variables d'environnement

Vous devez définir les variables pour connecter l'application à votre base de données PostgreSQL ainsi qu'à l'API Spoonacular.

  - [ ] Dans le dossier `backend`, Créez une copie du fichier .env.template que vous nommerez .env
  - [ ] Adaptez son contenu selon la configuration de votre base de données et les clés dont vous disposez

## Initialisation de la base de données

Après avoir créé votre base PostgreSQL et configuré le fichier `.env`, vous devez initialiser la base de données la toute première fois.

Dans un terminal à la racine du projet :

```bash
cd backend
uv run -m utils.reset_database.py
```

## Lancer l'application

Dans un terminal à la racine du projet :
```bash
cd backend
uv run main.py
```

<<<<<<< HEAD
L'API sera accessible sur http://localhost:8000.
(Si vous utilisez un service comme le VSCode d'un Datalab, pensez à ouvrir le port 8000 et à utiliser le lien fourni dans la documentation à l'ouverture du service plutôt que localhost).

Documentation de l'API (une fois lancée) :

Swagger UI : http://localhost:8000/docs
=======
L'API sera accessible sur http://localhost:5000.
(Si vous utilisez un service comme le VSCode d'un Datalab, pensez à ouvrir le port 5000 et à utiliser le lien fourni dans la documentation à l'ouverture du service plutôt que localhost).

Documentation de l'API (une fois lancée) :

Swagger UI : http://localhost:5000/docs
>>>>>>> origin/Kubernetes

## Lancer les tests

Dans un terminal :
```bash
uv run -m pytest
```

## Scénario d'utilisation

Dans le Swagger :

Créer un utilisateur en utilisant
`POST /utilisateurs/ Creer Utilisateur`

Se connecter :
- Soit en cliquant sur Authorize en haut à droite du Swagger
- Soit en utilisant une requête qui nécessite d'être connecté comme
`GET /utilisateurs/ Lister Utilisateurs`

La requête pour supprimer un utilisateur est réservé aux admins.

Les requêtes concernant la planification de repas et la liste de courses sont intuitives, suivre les instructions de chaque requête indiquée dans le Swagger.
