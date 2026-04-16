FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port for API
EXPOSE 8000
# Default port for UI
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Default command can be overridden to run API or UI
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
