# projet-conception-logicielle

Cette application permet de chercher des recettes de cuisine, de planifier ses repas et de générer une liste de courses, le tout à partir de son compte personnel utilisateur.

Ce projet met en œuvre :
- Git
- Architecture applicative (couches, IoC, SRP)
- Linting et qualité du code
- Tests unitaires
- CI/CD
- Design patterns et bonnes pratiques
- Docker, Kubernetes
- Authentification sécurisée
- Utilisation des API Spoonacular et Open Food Facts

## :arrow\_forward: Prérequis

Vous devez avoir installé uvicorn.

Pour toute la suite, vous devez avoir choisi comme **répertoire de travail** `backend`, à partir duquel les commandes seront exécutées.

## :arrow\_forward: Variables d'environnement

Vous devez définir les variables pour connecter l'application à votre base de données PostgreSQL ainsi qu'à l'API Spoonacular.

  - [ ] Créez une copie du fichier .env.template que vous nommerez .env
  - [ ] Adaptez son contenu selon la configuration de votre base de données et les clés dont vous disposez

## :arrow\_forward: Initialisation de la base de données

Après avoir créé votre base PostgreSQL et configuré le fichier `.env`, vous devez initialiser la base de données la toute première fois.

Dans un terminal :

```bash
uv run -m utils.reset_database.py
```

## :arrow\_forward: Lancer l'application

Dans un terminal :
```bash
uv run main.py
```
