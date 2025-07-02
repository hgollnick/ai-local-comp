import json
import shutil
import os
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

CONFIG_PATH = "agent_config.json"
BACKUP_PATH = "agent_config.json.bak"

default_config = {
    "router_model": "phi",
    "code_model": "codellama",
    "simple_model": "mistral",
    "complex_model": "llama3",
    "ollama_url": os.environ.get("OLLAMA_URL", "http://localhost:11434"),
    "use_langchain_router": False
}

class Config(BaseModel):
    router_model: str
    code_model: str
    simple_model: str
    complex_model: str
    ollama_url: str
    use_langchain_router: bool = False

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

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        logger.info(f"Saving config to {CONFIG_PATH}: {cfg}")
        json.dump(cfg, f, indent=2)