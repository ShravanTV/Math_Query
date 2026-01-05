# Frontend Service - Streamlit Web Interface

This service provides an interactive web interface for the Math Query Assistant using Streamlit.

The frontend is designed as a single-turn interaction interface rather than a conversational chatbot. Each question and its response are treated as independent pairs, with visual separation between different question-response sets.

### Key Features

- **Real-time Interaction**: Immediate feedback and response display
- **Error Handling**: Graceful handling of backend connectivity issues
- **Visual Separation**: Clear distinction between different question-response pairs


## Implementation Details

### Core Components

1. **Message Display Logic**: 
   - Iterates through session messages to create question-response pairs
   - Renders each pair with appropriate styling and alignment
   - Handles orphaned user messages (waiting for response)

2. **Input Handling**:
   - Uses Streamlit's chat input widget for natural interaction
   - Automatically adds user messages to session state
   - Triggers API calls to backend service

3. **API Communication**:
   - Sends POST requests to backend `/query` endpoint
   - Handles timeouts and connection errors
   - Displays error messages when backend is unavailable


### Interaction Flow

1. **Question Input**: User types question in chat input widget
2. **Immediate Display**: User question appears in green bubble (right-aligned)
3. **API Call**: Backend is contacted for response
4. **Response Display**: Model response appears in gray bubble (left-aligned)
5. **Visual Separation**: Horizontal line separates this pair from next interaction


## Error Handling

### Error Display

Error messages are displayed in the same format as regular responses, ensuring consistent user experience.

## Performance Considerations

### Session Management

- **Memory Usage**: Session state persists during browser session
- **State Reset**: Refreshing the page clears the conversation history
