
"""
FastAPI Backend Service for Math Query Assistant

This module provides a RESTful API gateway between client applications and the Ollama LLM service.
It handles request validation, communication with the LLM, error handling, and logging.

Key Features:
- POST /query endpoint for processing user questions
- Input validation and sanitization
- Comprehensive error handling and logging
- CORS support for web frontend integration
- Structured request/response models with Pydantic
"""

import os
import logging
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Configure logging for monitoring and debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ollama_api")

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Math Query Ollama Backend",
    description="API gateway for Math Query Assistant LLM service",
    version="1.0.0"
)

# Configure CORS middleware for cross-origin requests from web frontend
# In production, replace "*" with specific allowed origins for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development setting - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Ollama configuration from environment variables with sensible defaults
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "math-ping-assistant")

# Pydantic models for request/response validation and serialization
class QueryRequest(BaseModel):
    """Model for incoming query requests."""
    question: str

class QueryResponse(BaseModel):
    """Model for query responses."""
    response: str


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Process user question and return LLM response.
    
    This endpoint:
    1. Validates the input question
    2. Sends the question to the Ollama LLM service
    3. Returns the model's response or appropriate error message
    
    Args:
        request: QueryRequest containing the user's question
        
    Returns:
        QueryResponse containing the LLM's response
        
    Raises:
        HTTPException: For validation errors or service unavailability
    """
    # Clean and validate input
    question = request.question.strip()
    if not question:
        logger.warning("Received empty question.")
        return JSONResponse(
            status_code=400, 
            content={"response": "Question cannot be empty."}
        )
    
    # Prepare payload for Ollama API
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": question,
        "stream": False  # We want complete response, not streaming
    }
    
    try:
        # Log the incoming query for monitoring
        logger.info(f"Querying Ollama: {question}")
        
        # Make request to Ollama service with extended timeout for model inference
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=180)
        resp.raise_for_status()  # Raise exception for HTTP errors
        
        # Extract and clean the model response
        result = resp.json().get("response", "").strip()
        logger.info(f"Ollama response: {result}")
        
        return QueryResponse(response=result)
        
    except requests.exceptions.Timeout:
        error_msg = "Request to Ollama service timed out"
        logger.error(f"{error_msg}: {e}")
        return JSONResponse(
            status_code=504, 
            content={"response": f"Ollama service timeout: Request exceeded 180 seconds"}
        )
    except requests.exceptions.ConnectionError:
        error_msg = "Could not connect to Ollama service"
        logger.error(f"{error_msg}: {e}")
        return JSONResponse(
            status_code=502, 
            content={"response": "Ollama service unavailable: Connection refused"}
        )
    except Exception as e:
        # Catch-all for other unexpected errors
        logger.error(f"Ollama service error: {e}")
        return JSONResponse(
            status_code=502, 
            content={"response": f"Ollama service error: {str(e)}"}
        )



@app.get("/")
def root():
    """
    Root endpoint with service information.
    
    Returns:
        dict: Basic service information and available endpoints
    """
    return {
        "service": "Math Query Backend",
        "version": "1.0.0",
        "endpoints": {
            "query": "/query - POST endpoint for math questions"
        }
    }
