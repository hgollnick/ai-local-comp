import requests
import logging
from typing import List

logger = logging.getLogger(__name__)

def list_models() -> List[str]:
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        # The models are under the "models" key, each with a "name"
        return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return []