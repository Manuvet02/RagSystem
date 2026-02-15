FROM python:3.12-slim

WORKDIR /app

# Dipendenze di sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia TUTTO il progetto nella root /app
COPY . .

# Espone porta FastAPI
EXPOSE 8000

# Avvia FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]