"""
Model-related API endpoints.
Handles Ollama model management operations.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.models import ModelsResponse, PullModelResponse
from app.services.models import ModelService
from app.dependencies import get_model_service

logger = logging.getLogger("app.api.models")
router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=ModelsResponse)
async def list_models(
    model_service: ModelService = Depends(get_model_service)
) -> ModelsResponse:
    """
    Get list of available Ollama models.
    
    Returns all models currently available in the connected Ollama instance.
    """
    logger.info("Fetching available models")
    
    try:
        models = await model_service.list_models()
        logger.info(f"Found {len(models)} available models")
        return ModelsResponse(models=models)
        
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch models from Ollama"
        )
    finally:
        await model_service.close()


@router.post("/pull/{model_name}", response_model=PullModelResponse)
async def pull_model(
    model_name: str,
    model_service: ModelService = Depends(get_model_service)
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
