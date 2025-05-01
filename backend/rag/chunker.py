import os
import json
import uuid
import re
import xml.etree.ElementTree as ET

VIEWS_DIR = os.path.join(os.path.dirname(__file__), "views")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "chunks.jsonl")
MAX_VIEW_LENGTH = 15000
MAX_ELEMENT_LENGTH = MAX_VIEW_LENGTH

chunks = []
unique_tags = set()
count_views = 0
count_large_views = 0
count_elements = 0
count_skipped_elements = 0

def extract_elements(xml_content, title):
    element_chunks = []
    global count_skipped_elements
    try:
        root = ET.fromstring(xml_content)
        for elem in root.iter():
            tag = re.sub(r'\{.*\}', '', elem.tag)
            unique_tags.add(tag)
            element_str = ET.tostring(elem, encoding='unicode')
            if len(element_str) > MAX_ELEMENT_LENGTH:
                count_skipped_elements += 1
                continue
            element_chunks.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "type": tag,
                "code": element_str.strip()
            })
    except ET.ParseError as e:
        print(f"Fehler beim Parsen von {title}: {e}")
    return element_chunks

for filename in os.listdir(VIEWS_DIR):
    if filename.endswith(".view.xml"):
        path = os.path.join(VIEWS_DIR, filename)
        with open(path, encoding="utf-8") as f:
            xml_content = f.read().strip()

        view_title = filename.replace(".view.xml", "")

        if len(xml_content) <= MAX_VIEW_LENGTH:
            chunks.append({
                "id": str(uuid.uuid4()),
                "title": view_title,
                "type": "view",
                "code": xml_content
            })
            count_views += 1
        else:
            count_large_views += 1

        element_chunks = extract_elements(xml_content, view_title)
        chunks.extend(element_chunks)
        count_elements += len(element_chunks)

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for chunk in chunks:
        out.write(json.dumps(chunk, ensure_ascii=False) + "\n")

print(f"\n{len(chunks)} Chunks erfolgreich in {os.path.basename(OUTPUT_PATH)} geschrieben.\n")
print(f"Vollständige Views aufgenommen       : {count_views}")
print(f"Zu große Views (nicht aufgenommen)   : {count_large_views}")
print(f"Einzelne UI5-Elemente extrahiert     : {count_elements}")
print(f"Übersprungene Elemente wegen Länge   : {count_skipped_elements}")