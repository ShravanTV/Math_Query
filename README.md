# Math Query Assistant - Containerized LLM Solution

A comprehensive solution demonstrating precise AI behavior control using Ollama, Docker, and a modern web interface. This project implements a custom Large Language Model that follows strict behavioral rules for mathematical queries, ping-pong protocol, and input rejection.


## Features

- **Mathematical Query Response**: The LLM answers questions that are explicitly mathematical in nature
- **Ping-Pong Protocol**: Responds with "pong!!!" when user input is exactly "ping" (case-insensitive)
- **Strict Limitation**: Rejects all other inputs with a predefined response
- **Containerized Architecture**: Fully Docker-based deployment with 4 services
- **Web Interface**: Modern Streamlit frontend for user interaction
- **API Backend**: FastAPI-based backend service for model communication
- **Automated Testing**: Demo service with comprehensive test suite

## Architecture

The solution consists of 4 containerized services:

1. **Ollama Service** (`ollama/`): Hosts the custom math-ping-assistant model
2. **Backend Service** (`backend/`): FastAPI server handling API requests
3. **Frontend Service** (`frontend/`): Streamlit web interface
4. **Demo Service** (`demo_backend/`): Automated demonstration script

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Backend   │    │    Ollama   │
│  (Streamlit)│◄──►│  (FastAPI)  │◄──►│ (LLM Service)│
│   :8501     │    │    :8000    │    │   :11434    │
└─────────────┘    └─────────────┘    └─────────────┘
                           ▲
                           │
                   ┌─────────────┐
                   │  Demo Test  │
                   │   Service   │
                   └─────────────┘
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- At least 8GB RAM available for the Ollama service
- Network access to pull base Docker images

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Math_query
```

2. Build and start all services:
```bash
docker-compose up --build -d
```

3. Wait for all services to be ready (approximately 2-3 minutes for initial model loading)

### Accessing the Application

- **Web Interface**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Ollama API**: http://localhost:11434
- **API Documentation**: http://localhost:8000/docs

### Testing the System

The demo service automatically runs test cases and outputs results to a CSV file. View results:
```bash
docker-compose logs demo-backend
```

Or manually test via the web interface or API:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 10 divided by 2?"}'
```

## System Prompt Design

The custom Modelfile uses a carefully crafted system prompt with three distinct behavioral rules:

1. **Mathematical Queries**: Detects calculation requests and provides direct answers
2. **Ping-Pong Protocol**: Case-insensitive "ping" detection with exact "pong!!!" response
3. **Rejection Rule**: Consistent refusal message for all other inputs

### Model Configuration

- **Base Model**: `phi4-mini:3.8b` - Chosen for mathematical reasoning capabilities and efficient resource usage
- **Temperature**: 0.1 - Low temperature for deterministic, consistent behavior
- **Top-p**: 0.1 - Reduces randomness in token selection
- **Top-k**: 10 - Limits token choices for more predictable outputs

## Challenges and Solutions

### Challenge 1: Model Loading Time
**Problem**: Ollama loads models on first inference, causing initial delays
**Solution**: Implemented warm-up query during container startup to pre-load the model

### Challenge 2: Service Dependencies
**Problem**: Backend and frontend depend on Ollama being fully ready
**Solution**: Added health checks and startup delays in docker-compose.yml

### Challenge 3: Consistent Behavior
**Problem**: Ensuring the model strictly follows rules without variation
**Solution**: Careful parameter tuning and explicit system prompt with clear examples

## File Structure

```
Math_query_V2/
├── docker-compose.yml          # Orchestration of all services
├── README.md                   # This file
├── ollama/                     # Custom LLM service
│   ├── Modelfile              # Custom model configuration
│   ├── Dockerfile             # Ollama container setup
│   └── README.md              # Ollama service documentation
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   └── main.py           # API endpoints and logic
│   ├── Dockerfile            # Backend container
│   └── README.md             # Backend documentation
├── frontend/                   # Streamlit web interface
│   ├── app.py                # Frontend application
│   ├── Dockerfile            # Frontend container
│   └── README.md             # Frontend documentation
└── demo_backend/              # Testing and demonstration
    ├── demo_script.py        # Automated test suite
    ├── demo_results.csv      # Test results output
    ├── Dockerfile            # Demo service container
    └── DEMO_SCRIPT_README.md # Demo service documentation
```

## Usage Examples

### Mathematical Queries
- Input: "What is 10 divided by 2?"
- Output: "5"

### Ping-Pong Protocol
- Input: "ping" or "PING" or "Ping"
- Output: "pong!!!"

### Rejection Cases
- Input: "Tell me a story"
- Output: "I am designed to only answer mathematical questions or respond to 'ping'."

## Development Notes

- The system is designed for single-turn interactions, not conversational chat
- Each query is processed independently without context from previous interactions
- The frontend maintains session state for display purposes only
- All services are configured for development with CORS enabled
