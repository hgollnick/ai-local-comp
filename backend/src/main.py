from fastapi import FastAPI, Body
from src.config import Config, load_config, save_config
from src.models import list_models
from src.agents.router_agent import RouterAgent

app = FastAPI()

router_agent = RouterAgent()

@app.get("/models")
def get_models():
    return {"models": list_models()}

@app.get("/config", response_model=Config)
def get_config():
    return load_config()

@app.post("/config")
def set_config(cfg: Config):
    save_config(cfg.dict())
    return {"status": "ok"}

@app.post("/ask")
def ask_question(payload: dict = Body(...)):
    question = payload.get("question", "")
    if not question:
        return {"error": "No question provided."}
    answer, model = get_agent_answer_and_model(question)
    return {"answer": answer, "model": model}


def get_agent_answer_and_model(question: str):
    agent_type = router_agent.decide_agent(question)
    if agent_type == "code":
        answer = router_agent.code_agent.generate(question)
        model = router_agent.code_model
    elif agent_type == "simple":
        answer = router_agent.fast_agent.generate(question)
        model = router_agent.simple_model
    else:
        answer = router_agent.general_agent.generate(question)
        model = router_agent.complex_model
    return answer, model