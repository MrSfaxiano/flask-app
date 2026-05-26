FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching — only reruns if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ ./app/

EXPOSE 5000

CMD ["python", "-m", "app.main"]
