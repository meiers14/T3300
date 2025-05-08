import os
import uuid

PREVIEW_FOLDER = "backend/previews"

def generate_ui5_preview_html(xml: str) -> str:
    os.makedirs(PREVIEW_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex[:8]}.html"
    full_path = os.path.join(PREVIEW_FOLDER, filename)

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>UI5 Vorschau</title>
  <script
    src="https://openui5.hana.ondemand.com/resources/sap-ui-core.js"
    id="sap-ui-bootstrap"
    data-sap-ui-theme="sap_horizon"
    data-sap-ui-libs="sap.m,sap.ui.core,sap.ui.layout,sap.f,sap.tnt,sap.uxap"
    data-sap-ui-async="false">
  </script>
  <style>
    html, body, #content {{
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
    }}
    #error {{
      display: none;
      color: red;
      font-family: monospace;
      padding: 1em;
      background: #fff0f0;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      z-index: 1000;
    }}
  </style>
</head>
<body class="sapUiBody" id="content">

  <div id="error">Fehler beim Laden der Vorschau.</div>

  <script id="myView" type="ui5/xmlview">
    {xml}
  </script>

  <script>
    try {{
      sap.ui.getCore().attachInit(function () {{
        try {{
          sap.ui.xmlview({{
            viewContent: document.getElementById("myView").innerHTML
          }}).placeAt("content");
        }} catch (e) {{
          console.error("UI5 Fehler:", e);
          document.getElementById("error").textContent = "Fehler in der XML-Ansicht: " + e.message;
          document.getElementById("error").style.display = "block";
        }}
      }});
    }} catch (globalError) {{
      console.error("Globale Vorschau-Fehler:", globalError);
      document.getElementById("error").textContent = "Initialisierungsfehler: " + globalError.message;
      document.getElementById("error").style.display = "block";
    }}
  </script>
</body>
</html>
"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)

    return f"/preview/{filename}"