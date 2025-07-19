"""
Agent-related API endpoints.
Handles AI agent interactions and question processing.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from app.schemas.agent import AskRequest, AskResponse
from app.services.agents import RouterService
from app.dependencies import get_router_service

logger = logging.getLogger("app.api.agents")
router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    router_service: RouterService = Depends(get_router_service)
) -> AskResponse:
    """
    Ask a question to the AI agents.
    
    The system will automatically route the question to the most appropriate agent:
    - Code agent for programming-related questions
    - Simple agent for quick factual questions  
    - Complex agent for nuanced, multi-part questions
    """
    logger.info(f"Processing question: {request.prompt[:100]}...")
    
    try:
        result = await router_service.process(request.prompt, request.context)
        
        response = AskResponse(
            response=result["response"],
            model=result["model"],
            router="intern",  # For now, using internal router
            agent_type=result["agent_type"],
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
