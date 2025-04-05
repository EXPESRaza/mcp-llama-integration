from fastapi import FastAPI, Request, HTTPException
import json
import uvicorn
import logging
import requests
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define data models
class ContextRequest(BaseModel):
    query_text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    additional_context: Optional[Dict[str, Any]] = None

class ContextResponse(BaseModel):
    context_elements: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

class LlamaRequest(BaseModel):
    model: str = "llama3"  # Default model, update as needed
    prompt: str
    stream: bool = False
    options: Optional[Dict[str, Any]] = None

# Initialize FastAPI app
app = FastAPI(title="Model Context Protocol Server with Llama Integration")

# Llama API endpoint
LLAMA_API_URL = "http://localhost:11434/api/generate"

def query_llama(text: str) -> str:
    """Query local Llama model for information."""
    try:
        payload = {
            "model": "llama3",  # Update to match your specific model
            "prompt": text,
            "stream": False
        }
        
        logger.info(f"Querying Llama model with: {text}")
        response = requests.post(LLAMA_API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response from model")
        else:
            logger.error(f"Error from Llama API: {response.status_code} - {response.text}")
            return f"Error querying model: {response.status_code}"
            
    except Exception as e:
        logger.error(f"Exception when querying Llama: {str(e)}")
        return f"Error: {str(e)}"

@app.post("/context", response_model=ContextResponse)
async def get_context(request: ContextRequest):
    logger.info(f"Received context request: {request}")
    
    # Prepare a prompt for the Llama model
    prompt = f"""Please provide relevant information for the following query: 
    {request.query_text}
    
    Respond with factual, helpful information."""

    # Get response from Llama
    llama_response = query_llama(prompt)
    
    # Create a context element from the Llama response
    context_elements = [{
        "content": llama_response,
        "source": "llama_model",
        "relevance_score": 0.9
    }]
    
    logger.info("Context retrieved from Llama model")
    return ContextResponse(
        context_elements=context_elements,
        metadata={
            "processing_time_ms": 150,
            "model": "llama3",
            "query": request.query_text
        }
    )

@app.get("/health")
async def health_check():
    # Check if Llama API is accessible
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            return {"status": "healthy", "llama_status": "connected"}
        else:
            return {"status": "degraded", "llama_status": "unavailable"}
    except Exception as e:
        return {"status": "degraded", "llama_status": "error", "error": str(e)}

if __name__ == "__main__":
    logger.info("Starting Model Context Protocol server with Llama integration")
    uvicorn.run(app, host="0.0.0.0", port=8000)