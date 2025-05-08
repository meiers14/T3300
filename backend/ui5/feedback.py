import os
import uuid
import json
import time
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FEEDBACK_FOLDER = "backend/feedbacks"


def get_ui5_feedback(xml_versions: List[str], chat_history: List[Dict[str, str]]) -> dict:
    system_prompt = (
        "Du bist ein erfahrener SAP-UI5-Experte. Analysiere den übergebenen XML-Code "
        "und gib basierend auf dem Chatverlauf eine professionelle Kritik sowie "
        "einen klaren Verbesserungsvorschlag. Verwende reines XML, kein Markdown.\n"
        "Antwortformat:\nKritik: <Text>\nVorschlag:\n<mvc:View ...>...</mvc:View>"
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    latest_xml = xml_versions[-1]

    messages.append({
        "role": "user",
        "content": f"Dies ist der aktuelle XML-Code:\n{latest_xml}\nBitte gib Verbesserungsvorschläge und Kritik dazu."
    })

    try:
        start = time.perf_counter()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
        )
        duration_ms = int((time.perf_counter() - start) * 1000)
        result = response.choices[0].message.content.strip()

        if "Vorschlag:" in result:
            commentary, suggested_code = result.split("Vorschlag:", 1)
        else:
            commentary, suggested_code = result, ""

        return {
            "commentary": commentary.strip(),
            "suggested_code": suggested_code.strip(),
            "metadata": {
                "model": "gpt-3.5-turbo",
                "total_tokens": getattr(response.usage, "total_tokens", 0),
                "response_ms": duration_ms
            }
        }

    except Exception as e:
        return {
            "commentary": f"Fehler beim Verarbeiten der Anfrage:\n{str(e)}",
            "suggested_code": "",
            "metadata": {
                "error": str(e),
                "model": "gpt-3.5-turbo",
                "response_ms": 0
            }
        }


def generate_feedback_html(xml: str) -> str:
    os.makedirs(FEEDBACK_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex[:8]}.html"
    full_path = os.path.join(FEEDBACK_FOLDER, filename)
    safe_xml_js = json.dumps(xml)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Feedback zu generiertem UI5-Code</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    html, body {{
      height: 100vh;
      margin: 0;
      overflow: hidden;
      font-family: Arial, sans-serif;
      background: #f8f9fa;
    }}
    .container {{
      display: flex;
      height: 100%;
      gap: 1rem;
      padding: 1.5rem;
    }}
    .versions, .chat {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .card {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .card-body {{
      flex: 1;
      overflow-y: auto;
    }}
    .xml-card {{
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 1rem;
      font-family: Consolas, monospace;
      white-space: pre-wrap;
    }}
    .chat-box {{
      flex-grow: 1;
      overflow-y: auto;
      padding: 1rem;
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 6px;
      margin-bottom: 1rem;
    }}
    .chat-msg {{
      margin-bottom: 1rem;
    }}
    .chat-msg.user p {{
      background: #d9f3fb;
      padding: 0.5rem 1rem;
      border-radius: 10px;
      display: inline-block;
    }}
    .chat-msg.assistant p {{
      background: #fff3cd;
      padding: 0.5rem 1rem;
      border-radius: 10px;
      display: inline-block;
    }}
    textarea {{
      resize: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="versions">
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <span id="version-label">Original</span>
          <div>
            <button class="btn btn-sm btn-outline-secondary" id="prev-btn">&lt;</button>
            <button class="btn btn-sm btn-outline-secondary" id="next-btn">&gt;</button>
          </div>
        </div>
        <div class="card-body">
          <div class="xml-card" id="xmlDisplay"></div>
        </div>
      </div>
    </div>
    <div class="chat">
      <div class="card">
        <div class="card-body chat-box" id="chatLog"></div>
        <div class="p-3 border-top">
          <label for="userPrompt" class="form-label fw-bold">Frage oder Verbesserungsvorschlag:</label>
          <textarea id="userPrompt" class="form-control mb-2" rows="3" placeholder="z.B. Nutze VBox statt HBox …"></textarea>
          <button class="btn btn-warning w-100" id="submitFeedback">Senden</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const xmlDisplay = document.getElementById("xmlDisplay");
    const chatLog = document.getElementById("chatLog");
    const userPrompt = document.getElementById("userPrompt");
    const sendBtn = document.getElementById("submitFeedback");
    const versionLabel = document.getElementById("version-label");
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");

    const originalXml = {safe_xml_js};
    let versions = [{{ label: "Original", code: originalXml }}];
    let chatMessages = [];
    let currentIndex = 0;

    function updateDisplay() {{
      xmlDisplay.textContent = versions[currentIndex].code;
      versionLabel.textContent = versions[currentIndex].label;
    }}

    prevBtn.onclick = () => {{
      if (currentIndex > 0) {{
        currentIndex--;
        updateDisplay();
      }}
    }};

    nextBtn.onclick = () => {{
      if (currentIndex < versions.length - 1) {{
        currentIndex++;
        updateDisplay();
      }}
    }};

    sendBtn.onclick = async () => {{
      const prompt = userPrompt.value.trim();
      if (!prompt) return;
      userPrompt.value = "";

      chatLog.innerHTML += `<div class="chat-msg user"><p>${{prompt}}</p></div>`;
      chatMessages.push({{ role: "user", content: prompt }});

      try {{
        const response = await fetch("http://localhost:8000/review-ui5", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            versions: versions.map(v => v.code),
            messages: chatMessages
          }})
        }});

        const data = await response.json();
        const cleanComment = data.commentary.replace(/^Kritik:\\s*/i, "");
        chatLog.innerHTML += `<div class="chat-msg assistant"><p><strong>Kritik:</strong> ${{cleanComment}}</p></div>`;
        chatMessages.push({{ role: "assistant", content: data.commentary }});

        if (data.suggested_code) {{
          versions.push({{
            label: "Vorschlag " + versions.length,
            code: data.suggested_code
          }});
          currentIndex = versions.length - 1;
          updateDisplay();
        }}

        chatLog.scrollTop = chatLog.scrollHeight;
      }} catch (err) {{
        chatLog.innerHTML += `<div class="chat-msg assistant"><p>Fehler: ${{err.message}}</p></div>`;
      }}
    }};

    updateDisplay();
  </script>
</body>
</html>
"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)

    return f"/feedback/{filename}"