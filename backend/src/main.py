from fastapi import FastAPI, Body, Request
from fastapi.responses import StreamingResponse
from src.config import Config, load_config, save_config
from src.models import list_models, pull_model
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

@app.post("/pull_model/{model_name}")
def pull_model_endpoint(model_name: str):
    """Endpoint to pull a model from Ollama, streaming progress."""
    response = pull_model(model_name)
    def event_stream():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk
    return StreamingResponse(event_stream(), media_type="application/octet-stream")

def get_agent_answer_and_model(question: str):
    agent_type = router_agent.decide_agent(question)
    print(f"[main.py] Routing agent type: {agent_type}")
    if agent_type == "code":
        print(f"[main.py] Using code_agent with model: {router_agent.code_model}")
        answer = router_agent.code_agent.generate(question)
        model = router_agent.code_model
    elif agent_type == "simple":
        print(f"[main.py] Using fast_agent with model: {router_agent.simple_model}")
        answer = router_agent.fast_agent.generate(question)
        model = router_agent.simple_model
    else:
        print(f"[main.py] Using general_agent with model: {router_agent.complex_model}")
        answer = router_agent.general_agent.generate(question)
        model = router_agent.complex_model
    return answer, model