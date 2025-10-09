# Banqueo 

## Gestion de comptes bancaires (Console Python)

Banqueo est un programme console en Python permettant de simuler la gestion d’une banque simple.

Le projet vise à pratiquer la programmation orientée objet (POO), les bonnes pratiques de code et la gestion des interactions entre objets.

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

## Vérifier l'utilisateur Git actuel (global et local)

- Pour le configurer uniquement sur le projet, ne pas mettre `--global`:

```
# identifiant/username
git config user.name -> git config user.name "user_name"

# email 
git config user.email -> git config user.email "email"
```

## tests 

- Utilisation de unittest, run `python -m unittest tests.test_client`

## Logs 

- Hiérarchie des niveaux standards du module logging :
```
DEBUG	     logger.debug()	      
INFO	     logger.info()	      
WARNING	     logger.warning()	  
ERROR	     logger.error()	      
CRITICAL	 logger.critical()	 
```
