import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from backend.rag.search import search_similar_chunks

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def describe_layout(layout: list) -> str:
    types = [el.get("ui5Type", "Unknown") for el in layout]
    return " ".join(types)

def generate_ui5_code(layout_json: list) -> str:
    layout_desc = describe_layout(layout_json)
    context_chunks = search_similar_chunks(layout_desc, top_k=3)

    context_xml = "\n\n".join(
        f"// {chunk['title']}:\n{chunk['type'] or ''}" for chunk in context_chunks
    )

    prompt = f"""
    Du bist ein SAP-UI5-Experte. Erzeuge aus folgendem Figma-Layout (JSON) ein präzises, sauberes XML-View.

    Kontextuelle Beispiele:
    {context_xml}

    JSON:
    {json.dumps(layout_json, indent=2)}

    Regeln:
    - Nutze ausschließlich SAP.m-Controls (z. B. Dialog, Button, Input, VBox, HBox, Label, FileUploader)
    - Beachte layoutMode: "VERTICAL" ➝ VBox, "HORIZONTAL" ➝ HBox
    - Verwende keine toolbar-Elemente bei Dialogen, sondern beginButton / endButton
    - Verwende text exakt wie im JSON ("text": ...), falls vorhanden
    - Kein Markdown, kein ```xml – nur reiner XML-Code

    Struktur:
    <mvc:View xmlns:mvc="sap.ui.core.mvc" xmlns="sap.m">
        ...
    </mvc:View>
    """.strip()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()