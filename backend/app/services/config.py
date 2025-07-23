import os
import json
import shutil
import logging

CONFIG_PATH = "config.json"
BACKUP_PATH = "config.json.bak"

# Define a default config (adjust fields as needed)
default_config = {
    "router_model": "default-router",
    "code_model": "default-code",
    "simple_model": "default-simple",
    "complex_model": "default-complex",
    "ollama_url": "http://localhost:11434"
}

logger = logging.getLogger("app.services.config")

def save_config(cfg: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            logger.info(f"Loading config from {CONFIG_PATH}")
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"{CONFIG_PATH} not found. Creating a new config and backing up any existing file as {BACKUP_PATH}.")
        if os.path.exists(CONFIG_PATH):
            shutil.copy2(CONFIG_PATH, BACKUP_PATH)
        save_config(default_config)
        return default_config
