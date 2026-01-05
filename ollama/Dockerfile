FROM ollama/ollama:latest

# Copy Modelfile
COPY Modelfile /Modelfile

# Start ollama server and create the model on container startup
# ENTRYPOINT ["/bin/sh", "-c", "\
# ollama serve & \
# sleep 3 && \
# ollama create math-ping-assistant -f /Modelfile && \
# echo 'Warming up model...' && \
# ollama run math-ping-assistant 'Hello' || true && \
# wait \
# "]

# Start ollama server and create the model on container startup
ENTRYPOINT ["/bin/sh", "-c", "\
: \"${OLLAMA_MODEL:?OLLAMA_MODEL is not set}\" && \
ollama serve & \
sleep 3 && \
ollama create \"$OLLAMA_MODEL\" -f /Modelfile && \
echo \"Warming up model $OLLAMA_MODEL...\" && \
ollama run \"$OLLAMA_MODEL\" 'Hello' || true && \
wait \
"]