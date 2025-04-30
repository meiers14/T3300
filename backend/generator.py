import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ui5_code(layout_json):
    prompt = f"""
        Du bist ein SAP-UI5-Experte. Erzeuge aus folgendem Figma-Layout (JSON) ein präzises, sauberes XML-View:

        JSON:
        {layout_json}

        Regeln:
        - Nutze ausschließlich SAP.m-Controls (z. B. Dialog, Button, Input, VBox, HBox, Label, FileUploader)
        - Beachte layoutMode: "VERTICAL" ➝ VBox, "HORIZONTAL" ➝ HBox
        - Verwende keine toolbar-Elemente bei Dialogen, sondern beginButton / endButton
        - Verwende text exakt wie im JSON ("text": ...)
        - Keine Icons, keine Platzhalter
        - Kein Markdown, kein ```xml - nur reiner XML-Code

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
