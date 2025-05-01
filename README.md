# UI5 Code Generator – Backend

## Voraussetzungen

- Docker & Docker Compose
- OpenAI API Key
- Pinecone API Key (Free Plan ausreichend)
- `.env`-Datei mit folgenden Einträgen:

```env
OPENAI_API_KEY=...
PINECONE_API_KEY=...
```

---

## Projektstruktur (Auszug)

```
backend/
  ├─ main.py                 # FastAPI-Anwendung
  ├─ generator.py            # GPT-gestützte Codegenerierung
  └─ rag/
      ├─ indexer.py          # Einmalige Indexierung der Chunks in Pinecone
      ├─ search.py           # Pinecone-Abfragen zur Kontextsuche
      ├─ chunker.py          # Zerlegung großer Views in sinnvolle Chunks
      ├─ chunks.jsonl        # Gechunkte UI5-Daten (XML + einzelne Elemente)
      └─ views/              # XML-Views aus OpenUI5
```

---

## Initialisierung

### 1. Repository klonen

```bash
git clone https://github.com/meiers14/T3300.git
cd PoC
```

### 2. `.env` erstellen

```bash
cp .env.example .env
# Dann OPENAI_API_KEY und PINECONE_API_KEY eintragen
```

### 3. Backend & API starten

```bash
docker compose up --build
```

FastAPI ist anschließend verfügbar unter [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Chunks erstellen

Wenn du neue Views hast oder die Chunklogik ändern willst:

```bash
docker compose exec backend python backend/rag/chunker.py
```

Dies erzeugt die Datei `chunks.jsonl` basierend auf allen XML-Dateien im `views/`-Ordner.

---

## Index aufbauen

Nur beim ersten Start oder nach Änderungen der `chunks.jsonl`:

```bash
docker compose exec backend python backend/rag/indexer.py
```

> Falls der Pinecone-Index noch nicht existiert, wird er automatisch erstellt.

---

## API-Endpunkt

### POST `/generate-ui5`

