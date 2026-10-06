# Banqueo 

## Gestion de comptes bancaires (Console Python)

Banqueo est un programme console en Python permettant de simuler la gestion 
d’une banque simple.

Le projet vise à pratiquer la programmation orientée objet (POO), les bonnes 
pratiques de code et la gestion des interactions entre objets.

Les utilisateurs pourront:
- Créer des clients et leurs comptes bancaires
- Déposer ou retirer de l’argent
- Effectuer des transferts entre comptes
- Consulter l’historique des opérations de chaque compte


## Objectif

- POO en Python: classes, objets, encapsulation, méthodes
- logique métier : validation de transactions, gestion des erreurs
- bonnes pratiques : architecture modulaire, tests simples, documentation
- Versionner le projet avec Git et gérer un environnement isolé `venv`


## Prérequis 

- Python 3.11.9
- Pip 24.0


## Créer un environnement virtuel

```
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Désactiver l'environnement
deactivate
```


## Installer des packages 

```
# Installer un package
pip install nom_du_package

# Créer requirements.txt
pip freeze > requirements.txt

# Installer à partir de requirements.txt
pip install -r requirements.txt
```


## tests 

- Utilisation de unittest, run `python -m unittest tests.test_client`


## Logs 

- Hiérarchie des niveaux standards du module logging :
```
DEBUG	     logger.debug()	      
INFO	     logger.info()	      
WARNING	   logger.warning()	  
ERROR	     logger.error()	      
CRITICAL	 logger.critical()	 
```

## API 

### Installation de FastAPI

- Dans `venv` activé, installer Python FastAPI :
`pip install fastapi "uvicorn[standard]"`

- Lancer le serveur sur port 8001: `uvicorn api:app --reload --port 8001`
- Mettre à jour les dépendances : `requirements.txt` : `pip freeze > requirements.txt`

- Swagger UI (tests des endpoints) : http://127.0.0.1:8001/docs
- ReDoc (lecture seule) : http://127.0.0.1:8001/redoc


### Structure de l'API

- `api.py` : interface web, à côté de `main.py` : interface console
- Les deux utilisent la logique métier du dossier `bank/`
- Modèles Pydantic `ClientIn`, `AccountIn` : ils décrivent le JSON accepté
  par l'API et le valident (erreur 422 si le format est incorrect)
- Les `ValueError` levées par `bank/` sont converties en codes HTTP (404, 409)

Les données sont en mémoire : elles sont perdues au redémarrage du serveur 
(pour l'instant)


### Tests

Lancer les tests : `python -m unittest discover`