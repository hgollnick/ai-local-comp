import json
from pydantic import BaseModel

CONFIG_PATH = "agent_config.json"

default_config = {
    "router_model": "phi",
    "code_model": "codellama",
    "simple_model": "mistral",
    "complex_model": "llama3",
    "ollama_url": "http://localhost:11434"
}

class Config(BaseModel):
    router_model: str
    code_model: str
    simple_model: str
    complex_model: str
    ollama_url: str

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_config(default_config)
        return default_config

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)