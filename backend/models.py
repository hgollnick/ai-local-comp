import requests

def list_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        # The models are under the "models" key, each with a "name"
        return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        return []