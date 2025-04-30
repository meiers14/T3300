import os
import json
import uuid

VIEWS_DIR = os.path.join(os.path.dirname(__file__), "views")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "view_chunks.jsonl")

chunks = []

for filename in os.listdir(VIEWS_DIR):
    if filename.endswith(".view.xml"):
        path = os.path.join(VIEWS_DIR, filename)
        with open(path, encoding="utf-8") as f:
            xml = f.read().strip()

        chunks.append({
            "id": str(uuid.uuid4()),
            "title": filename.replace(".view.xml", ""),
            "type": "view",
            "code": xml
        })

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for chunk in chunks:
        out.write(json.dumps(chunk, ensure_ascii=False) + "\n")

print(f"{len(chunks)} Chunks erfolgreich nach view_chunks.jsonl geschrieben.")
