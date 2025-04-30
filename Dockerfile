# 1. Basis-Image
FROM python:3.11-slim

# 2. Arbeitsverzeichnis im Container
WORKDIR /app

# 3. Kopiere PoC-Code ins Image
COPY backend/ ./backend/
COPY .env .
COPY requirements.txt .

# 4. Installiere Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# 5. Exponiere den Port
EXPOSE 8000

# 6. Starte Uvicorn-Server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
