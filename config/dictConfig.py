import os
import logging.config

# Crée le dossier logs/ si nécessaire
os.makedirs("logs", exist_ok=True)

LOG_FILE = os.path.join("logs", "app.log")  

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default", "level": "INFO"},
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "level": "DEBUG",
            "filename": LOG_FILE,  # chemin complet
            "mode": "a",           # ajouter au fichier existant
        },
    },
    "loggers": {
        "bank": {"handlers": ["console", "file"], "level": "DEBUG"},
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("bank")
