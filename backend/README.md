# Backend Service - FastAPI Gateway

This service provides a FastAPI-based backend that acts as a gateway between client applications and the Ollama LLM service. It handles API requests, validates input, manages communication with the LLM, and provides error handling and logging.

## Architecture Overview

The backend service is built with FastAPI and serves as the central API layer for the Math Query Assistant system.

### Key Components

- **Request Validation**: Pydantic models for input/output validation
- **Error Handling**: Comprehensive error responses and logging
- **Service Communication**: HTTP client for Ollama API integration

## API Documentation

### Primary Endpoint

#### POST /query
Processes user questions and returns model responses.

**Request Body:**
```json
{
  "question": "What is 10 divided by 2?"
}
```

**Response Format:**
```json
{
  "response": "5"
}
```


### OpenAPI Documentation
Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama service endpoint |
| `OLLAMA_MODEL` | `math-ping-assistant` | Custom model name |

### Service Dependencies

The backend depends on:
- **Ollama Service**: Must be running and healthy before backend starts
- **Network Access**: Must be able to reach Ollama API endpoint

## Implementation Details

### Request Processing Flow

1. **Input Validation**: 
   - Checks for empty or whitespace-only questions
   - Returns 400 error for invalid input

2. **Ollama Communication**:
   - Constructs payload with model name and prompt
   - Makes POST request to `/api/generate` endpoint
   - Sets 180-second timeout for model inference

3. **Response Handling**:
   - Extracts model response from JSON
   - Logs interaction details
   - Returns structured response to client

4. **Error Management**:
   - Catches network timeouts and connection errors
   - Logs detailed error information
   - Returns appropriate HTTP status codes



### Input Validation
- Strips whitespace from user input
- Rejects empty questions to prevent unnecessary API calls
- Uses Pydantic for type safety and validation

### Error Information
- Generic error messages to prevent information leakage
- Detailed logging for debugging purposes
- No stack traces exposed to clients

## Performance Features

### Logging
Comprehensive logging at INFO level:
- Request questions received
- Ollama responses returned
- Error conditions and exceptions

### Timeout Handling
- 180-second timeout for Ollama requests
- Prevents hanging connections
- Graceful error handling for timeouts



## Usage Examples

### Direct API Testing
```bash
# Mathematical query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 15 + 27?"}'

# Ping test
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "ping"}'

# Rejection test
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me a joke"}'
```