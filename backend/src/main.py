import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Debugpy is listening on 0.0.0.0:5678")

import logging
from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import StreamingResponse
import time

from src.config import Config, load_config, save_config
from src.models import list_models, pull_model
from backend.src.agent.basic.router_agent import RouterAgent
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, filename="backend.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s")
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

@app.get("/logs/stream")
def stream_logs():
    """
    Streams the last 100 lines from backend.log, then follows new lines in real time (like tail -n 100 -f), using Server-Sent Events (SSE).
    """
    import os
    from fastapi import Response
    def tail_lines(filename, n=100):
        """Read the last n lines from a file efficiently."""
        try:
            with open(filename, 'rb') as f:
                f.seek(0, os.SEEK_END)
                end = f.tell()
                lines = []
                size = 0
                block = 1024
                while end > 0 and len(lines) <= n:
                    delta = min(block, end)
                    f.seek(end - delta, os.SEEK_SET)
                    buf = f.read(delta)
                    lines = buf.split(b'\n') + lines
                    end -= delta
                return [l.decode(errors='replace') + '\n' for l in lines[-n:] if l]
        except Exception as e:
            return [f"Error reading log file: {e}\n"]
    def event_stream():
        logfile = "backend.log"
        if not os.path.exists(logfile):
            yield f"data: Log file not found.\n\n"
            return
        # Yield last 100 lines first
        for line in tail_lines(logfile, 100):
            yield f"data: {line.rstrip()}\n\n"
        try:
            with open(logfile, "r") as f:
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        yield f"data: {line.rstrip()}\n\n"
                    else:
                        time.sleep(0.5)
        except Exception as e:
            yield f"data: Error reading log file: {e}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")