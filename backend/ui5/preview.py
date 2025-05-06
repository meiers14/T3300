import os
import uuid

PREVIEW_FOLDER = "backend/previews"

# TODO: Löschen der generierten HTML-Dateien
# TODO: Fehlerbehandlung, wenn die HTML-Datei im Frontend nicht geladen werden kann

def generate_ui5_preview_html(xml: str) -> str:
    os.makedirs(PREVIEW_FOLDER, exist_ok=True)
  
    filename = f"preview-{uuid.uuid4()}.html"
    full_path = os.path.join(PREVIEW_FOLDER, filename)

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
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
    }}
  </style>
</head>
<body class="sapUiBody" id="content">
  <script id="myView" type="ui5/xmlview">
    {xml}
  </script>
  <script>
    sap.ui.getCore().attachInit(function () {{
      sap.ui.xmlview({{
        viewContent: document.getElementById("myView").innerHTML
      }}).placeAt("content");
    }});
  </script>
</body>
</html>"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)

    return f"/static/{filename}"