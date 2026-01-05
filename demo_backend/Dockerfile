FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY demo_script.py ./
CMD ["sh", "-c", "sleep 120 && python demo_script.py"]

