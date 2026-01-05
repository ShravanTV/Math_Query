# Ollama Service - Custom Math Query Model

This service hosts the custom `math-ping-assistant` model using Ollama.

## Model Configuration

### Base Model Selection
The service uses `llama3.2:3b` as the base model for the following reasons:

- **Strong Performance**: Llama 3.2 3B consistently outperforms competing models like Gemma 2 2.6B and Phi 3.5-mini on the IFEval benchmark, which specifically tests the ability to follow complex, verifiable constraints (e.g., "only answer math questions").
- **Mathematical Capability**: Eventhough other models like Phi4-mini demonstrates strong reasoning capabilities, especially in mathematics and logic, Llama 3.2 3B is more factual and follows "negative" instructions (what not to do) with higher reliability.
- **Resource Efficiency**: At 3B parameters, it's optimized for local deployment with lower memory requirements
- **Fast Inference**: Smaller model size enables quicker response times for real-time interactions


### Parameter Tuning

#### Temperature: 0.1
**Purpose**: Ensures deterministic, consistent behavior
**Rationale**: Low temperature reduces randomness in token selection, which is critical for:
- Maintaining exact "pong!!!" response for ping inputs
- Providing consistent mathematical answers without variation
- Ensuring the rejection message remains identical across non-math queries

#### Top-p: 0.1
**Purpose**: Constrains token selection to high-probability options
**Rationale**: 
- Reduces creative variation that could break the strict behavioral rules
- Focuses the model on the most likely correct mathematical answers
- Prevents deviation from the predefined response patterns

#### Top-k: 10
**Purpose**: Limits the token selection pool
**Rationale**:
- Further constrains output possibilities for more predictable behavior
- Balances between necessary flexibility for math problems and strict adherence to rules
- Optimizes performance by reducing computational overhead

## System Prompt Design

The system prompt is engineered to enforce three distinct behavioral modes through explicit rule-based instructions:

### Rule 1: Mathematical Queries
```
If the user asks a question requiring mathematical calculation (contains math terms, numbers with operations, or calculation requests), provide only the answer.
```
**Design Philosophy**: 
- Direct, no-explanation responses for mathematical calculations
- Examples guide the model toward concise answers
- Eliminates conversational elements for pure computational responses

### Rule 2: Ping-Pong Protocol
```
If the user input is exactly "ping" (ignore case), respond with exactly "pong!!!".
```
**Design Philosophy**:
- Case-insensitive detection ensures robustness
- Exact response specification eliminates variation
- Simple protocol demonstrates precise input-output control

### Rule 3: Rejection Rule
```
For ALL other inputs that are not mathematical or "ping", respond EXACTLY: "I am designed to only answer mathematical questions or respond to 'ping'."
```
**Design Philosophy**:
- Comprehensive catch-all for non-conforming inputs
- Consistent refusal message maintains system boundaries
- Clear communication of system limitations

## Docker Implementation

### Container Setup
The Dockerfile performs these critical operations:

1. **Base Image**: Uses official `ollama/ollama` image
2. **Model Creation**: Automatically creates the custom model from the Modelfile
3. **Warm-up Query**: Executes a sample question during startup to:
   - Load the model into memory
   - Initialize GPU/CPU allocation
   - Apply model layers/adapters
   - Eliminate first-query latency for users

### Startup Process
Executing docker compose automatically creates the custom model and executes a sample question to warm up the model.


### Environment Variables
- `OLLAMA_MODEL=math-ping-assistant`: Specifies the custom model name
- Used by backend service to reference the correct model

### Port Exposure
- **11434**: Standard Ollama API port for external service communication

## API Endpoints

The service exposes standard Ollama endpoints:


## Performance Considerations

### Memory Requirements
- **Minimum**: 8GB RAM for model loading

### Response Times
- **Cold Start**: 2-3 seconds (model loading)
- **Warm Queries**: <1 second for typical math questions
- **Ping Response**: <500ms (simple pattern matching)

### Scaling Considerations
- Single model instance serves multiple concurrent requests
- Model remains in memory after warm-up
- Horizontal scaling requires multiple Ollama instances

## Troubleshooting

### Common Issues

1. **Model Not Found**
   - Check Modelfile syntax
   - Verify model creation in Docker logs
   - Ensure sufficient disk space

2. **Slow First Response**
   - Warm-up query should mitigate this
   - Check system resources
   - Verify GPU acceleration is working

3. **Inconsistent Behavior**
   - Review temperature and sampling parameters
   - Check system prompt for ambiguity
   - Verify no conflicting instructions

### Debug Commands
```bash
# Check model status
docker exec <container> ollama list

# Test model directly
docker exec <container> ollama run math-ping-assistant "ping"

# View logs
docker logs <container>
```

## Integration Notes

This service is designed to be called by:
- **Backend Service**: Primary consumer via HTTP API
- **Demo Service**: For automated testing
- **Direct API Access**: For development and debugging
