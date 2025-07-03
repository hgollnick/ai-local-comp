import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Debugpy is listening on 0.0.0.0:5678")

import logging
from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import StreamingResponse
from src.config import Config, load_config, save_config
from src.models import list_models, pull_model
from src.agents.router_agent import RouterAgent
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

router_agent = RouterAgent()

class AskRequest(BaseModel):
    prompt: str

@app.get("/models")
def get_models():
    logger.info("GET /models called")
    models = list_models()
    logger.info(f"Models available: {models}")
    return {"models": models}

@app.get("/config", response_model=Config)
def get_config():
    logger.info("GET /config called")
    config = load_config()
    logger.info(f"Config loaded: {config}")
    return config

@app.post("/config")
def set_config(cfg: Config):
    logger.info(f"POST /config called with: {cfg}")
    save_config(cfg.dict())
    logger.info("Config saved.")
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest):
    logger.info(f"POST /ask called with payload: {request}")
    question = request.prompt
    cfg = load_config()
    use_langchain = cfg.get("use_langchain_router", False)
    router = "langchain" if use_langchain else "intern"
    logger.info(f"Router used: {router}")
    result = router_agent.run(question)
    logger.info(f"Result: {result}")
    return {"response": result.get("response"), "model": result.get("model"), "router": router}

@app.post("/pull_model/{model_name}")
def pull_model_endpoint(model_name: str):
    logger.info(f"POST /pull_model/{model_name} called")
    response = pull_model(model_name)
    if response.status_code != 200:
        logger.error(f"Failed to pull model {model_name}: {response.status_code} {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)
    def event_stream():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                logger.debug(f"Streaming chunk of size {len(chunk)} for model {model_name}")
                yield chunk
    return StreamingResponse(event_stream(), media_type="application/octet-stream")