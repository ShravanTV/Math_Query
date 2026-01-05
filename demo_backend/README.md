# Demo Service - Automated Testing Suite

This service provides comprehensive automated testing for the Math Query Assistant system. It acts as a test suite that validates the three core behavioral rules of the custom LLM model and generates detailed reports of system performance.

## Purpose and Functionality

The demo service is designed to:
- **Automate Testing**: Run comprehensive test cases without manual intervention
- **Generate Reports**: Create CSV documentation of test results for analysis
- **Demonstrate Integration**: Showcase the complete system workflow


## Test Suite Design

### Test Categories

The test suite covers all three behavioral rules:

1. **Mathematical Queries**: Tests mathematical reasoning and calculation accuracy
2. **Ping-Pong Protocol**: Validates case-insensitive ping detection and exact response
3. **Rejection Rule**: Ensures non-math, non-ping inputs are properly rejected


## Implementation Details

### Execution Flow

1. **Service Initialization**: 
   - Waits for dependent services to be ready
   - Configures backend URL from environment variables

2. **Test Execution**:
   - Iterates through predefined test cases
   - Sends each question to the backend API
   - Captures and logs responses
   - Handles connection errors and timeouts

3. **Result Processing**:
   - Formats results for console output
   - Generates CSV report with detailed information

4. **Report Generation**:
   - Creates `demo_results.csv` with comprehensive test data
   - Includes description, question, expected behavior, and actual response
   - Provides persistent record of system performance


## Startup Delay Strategy

### 120-Second Delay Rationale

The service intentionally includes a 120-second delay before executing tests:

```python
# In docker-compose.yml (commented entrypoint)
entrypoint: ["/bin/sh", "-c", "sleep 120 && python demo_script.py"]
```

**Purpose of Delay**:
1. **Ollama Model Loading**: Ensures the custom model is fully downloaded and loaded
2. **Service Health**: Allows all dependent services to become healthy and responsive
3. **Model Warm-up**: Gives time for the warm-up query to complete in the Ollama service
4. **Network Stabilization**: Ensures Docker networking is fully established
5. **Resource Allocation**: Allows system resources to be allocated properly




## Usage and Integration

### Running Tests

```bash
# With docker-compose
docker-compose up demo-backend

# View results
docker-compose logs demo-backend

# Access CSV report
docker cp <container>:/app/demo_results.csv ./demo_results.csv
```

### Manual Test Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Set backend URL
export BACKEND_URL=http://localhost:8000/query

# Run tests
python demo_script.py
```
