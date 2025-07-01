import logging
from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import StreamingResponse
from src.config import Config, load_config, save_config
from src.models import list_models, pull_model
from src.agents.router_agent import RouterAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

router_agent = RouterAgent()

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
def ask_question(payload: dict = Body(...)):
    logger.info(f"POST /ask called with payload: {payload}")
    question = payload.get("question", "")
    if not question:
        logger.warning("No question provided in /ask payload.")
        return {"error": "No question provided."}
    answer, model = get_agent_answer_and_model(question)
    logger.info(f"Answer: {answer}, Model: {model}")
    return {"answer": answer, "model": model}

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

def get_agent_answer_and_model(question: str):
    logger.info(f"Routing question: {question}")
    agent_type = router_agent.decide_agent(question)
    logger.info(f"Routing agent type: {agent_type}")
    if agent_type == "code":
        logger.info(f"Using code_agent with model: {router_agent.code_model}")
        answer = router_agent.code_agent.generate(question)
        model = router_agent.code_model
    elif agent_type == "simple":
        logger.info(f"Using fast_agent with model: {router_agent.simple_model}")
        answer = router_agent.fast_agent.generate(question)
        model = router_agent.simple_model
    else:
        logger.info(f"Using general_agent with model: {router_agent.complex_model}")
        answer = router_agent.general_agent.generate(question)
        model = router_agent.complex_model
    logger.info(f"Final answer: {answer}, model: {model}")
    return answer, model