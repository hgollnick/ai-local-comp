from app.schemas.models import ListModelsResponse, PullModelResponse
from app.services.llm_models import LLMModelService
from app.dependencies import get_model_service


"""
Model-related API endpoints.
Handles AI interactions and question processing.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.ollama import AskRequest, AskResponse
from app.services.llm_model_selector import LLMModelSelectorService
from app.dependencies import get_router_service

logger = logging.getLogger("app.api.ollama")
router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    router_service: LLMModelSelectorService = Depends(get_router_service)
) -> AskResponse:
    """
    Ask a question to the Ollama.
    
    The system will automatically route the question to the most appropriate model:
    - Code model for programming-related questions
    - Simple model for quick factual questions  
    - Complex model for nuanced, multi-part questions
    """
    logger.info(f"Processing question: {request.prompt[:100]}...")
    
    try:
        result = await router_service.process(request.prompt, request.context)
        
        response = AskResponse(
            response=result["response"],
            model=result["model"],
            router="intern",  # For now, using internal router
            llm_model_type=result["llm_model_type"],
            processing_time=result.get("processing_time")
        )
        
        logger.info(f"Response generated successfully in {response.processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing ask request: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process request: {str(e)}"
        )


@router.get("/models", response_model=ListModelsResponse)
async def list_models(
    model_service: LLMModelService = Depends(get_model_service)
) -> ListModelsResponse:
    """
    Get list of available AI models.
    Returns all models currently available in the connected AI instance.
    """
    logger.info("Fetching available models")
    try:
        models = await model_service.list_models()
        logger.info(f"Found {len(models)} available models")
        return ListModelsResponse(models=models)
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch models from Ollama"
        )
    finally:
        await model_service.close()


@router.post("/models/pull/{model_name}", response_model=PullModelResponse)
async def pull_model(
    model_name: str,
    model_service: LLMModelService = Depends(get_model_service)
) -> PullModelResponse:
    """
    Pull a model from the Ollama registry.
    Downloads and installs the specified model if it's not already available.
    """
    logger.info(f"Pulling model: {model_name}")
    try:
        # Check if model already exists
        if await model_service.model_exists(model_name):
            return PullModelResponse(
                status="success",
                message=f"Model {model_name} already exists",
                model_name=model_name
            )
        result = await model_service.pull_model(model_name)
        return PullModelResponse(
            status="success",
            message=f"Model {model_name} pulled successfully",
            model_name=model_name
        )
    except Exception as e:
        logger.error(f"Error pulling model {model_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to pull model {model_name}: {str(e)}"
        )
    finally:
        await model_service.close()