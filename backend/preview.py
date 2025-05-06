from fastapi.responses import HTMLResponse

def generate_ui5_preview_html(xml: str) -> HTMLResponse:
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script
    src="https://openui5.hana.ondemand.com/resources/sap-ui-core.js"
    id="sap-ui-bootstrap"
    data-sap-ui-theme="sap_horizon"
    data-sap-ui-libs="sap.m,sap.ui.core"
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
    return HTMLResponse(content=html, status_code=200)
