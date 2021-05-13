# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:31:43 2021

Config file to all the configurations

@author: Abinaya.M02
"""

# Import necessary libraries
import logging
import logging.config
import sys
from pathlib import Path

from rich.logging import RichHandler
from simpletransformers.classification import ClassificationArgs

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, "config")
LOGS_DIR = Path(BASE_DIR, "logs")
DATA_DIR = Path(BASE_DIR, "data")
MODEL_DIR = Path(BASE_DIR, "model")
STORES_DIR = Path(BASE_DIR, "stores")
CACHE_DIR = Path(DATA_DIR, "cache")
BEST_MODEL_DIR = Path(MODEL_DIR, "{}/best_model")
OUTPUT_DIR = Path(DATA_DIR, "output")

# Local stores
BLOB_STORE = Path(STORES_DIR, "blob_store")
FEATURE_STORE = Path(STORES_DIR, "feature_store")
MODEL_REGISTRY = Path(STORES_DIR, "model_store")

# Create dirs
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
STORES_DIR.mkdir(parents=True, exist_ok=True)
BLOB_STORE.mkdir(parents=True, exist_ok=True)
FEATURE_STORE.mkdir(parents=True, exist_ok=True)
MODEL_REGISTRY.mkdir(parents=True, exist_ok=True)

# Set up logging
# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "info", "error"],
            "level": logging.INFO,
            "propagate": True,
        },
    },
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# Random seed
RANDOM_SEED = 100

# wandb directory (change the names as per need)
WANDB_PROJ_COMPLETE_DATA = "model_complete_data"
WANDB_PROJ_AL_BASELINE = "model_al_baseline"
WANDB_PROJ_AL_EXP = "model_al_experiments"

# Model args for the simpletransformer model
# Add or modify parameters bases on experiment
BEST_MODEL_SPEC_DIR = str(BEST_MODEL_DIR).format(WANDB_PROJ_AL_EXP)
MODEL_ARGS = ClassificationArgs(
    num_train_epochs=5,
    overwrite_output_dir=True,
    train_batch_size=16,
    max_seq_length=250,
    # modify based on the experiment
    wandb_project=WANDB_PROJ_AL_EXP,
    best_model_dir=BEST_MODEL_SPEC_DIR,
    cache_dir=CACHE_DIR,
    eval_batch_size=16,
    evaluate_during_training=True,
    evaluate_during_training_verbose=True,
    manual_seed=100,
    output_dir=OUTPUT_DIR,
    use_early_stopping=True,
    early_stopping_patience=3,
    reprocess_input_data=True,
)

# Model name (roberta-base, roberta-base-uncased, etc)
MODEL_NAME = "roberta"
MODEL_TYPE = "roberta-base"

# Labels for classification
LABELS = {"0": "Not sure", "1": "World", "2": "Sports", "3": "Business", "4": "Sci/Tech"}
TEST_SPLIT = 0.2
