figma.showUI(__html__, { width: 1000, height: 600 });

async function sendToBackend(mapped) {
  const response = await fetch("http://localhost:8000/generate-ui5", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ layout: mapped })
  });
  return await response.json();
}

function traverse(node) {
  if (!node.visible) return null;
  const name = (node.name || "").toLowerCase();
  const exclude = ["resize-corner", "placeholder", "badge decorative", "icon background"];
  if (exclude.some(e => name.includes(e))) return null;
  const obj = {
    id: node.id,
    name: node.name || "",
    type: node.type,
    layoutMode: node.layoutMode || null,
    characters: "characters" in node ? node.characters.trim() : "",
    children: []
  };
  if ("children" in node && Array.isArray(node.children)) {
    obj.children = node.children.map(traverse).filter(Boolean);
  }
  return obj;
}

function mapFigmaToUI5(node) {
  const name = (node.name || "").toLowerCase();
  const type = node.type;
  const layout = node.layoutMode;
  if (name.includes("title") && type === "TEXT") return "Title";
  if (name.includes("label") && type === "TEXT") return "Label";
  if (name.includes("input")) return "Input";
  if (name.includes("textarea")) return "TextArea";
  if (name.includes("upload")) return "FileUploader";
  if (name.includes("table")) return "Table";
  if (name.includes("list")) return "List";
  if (name.includes("dialog")) return "Dialog";
  if (name.includes("toolbar") || name.includes("footer")) return "Toolbar";
  if (name.includes("slot")) return "HTML";
  if (name.includes("status") || name.includes("badge")) return "ObjectStatus";
  if (name.includes("button") || ["ok", "cancel", "action"].some(k => name.includes(k))) return "Button";
  if (["FRAME", "GROUP"].includes(type)) {
    if (layout === "VERTICAL") return "VBox";
    if (layout === "HORIZONTAL") return "HBox";
  }
  if (type === "TEXT") return "Label";
  if (type === "RECTANGLE") return "Input";
  return "Unknown";
}

function mapTreeToUI5(node) {
  const ui5Type = mapFigmaToUI5(node);
  const hasChildren = node.children && node.children.length > 0;
  if (ui5Type === "Unknown" && !hasChildren) return null;
  let children = (node.children || []).map(mapTreeToUI5).filter(Boolean);
  let text = node.characters || "";
  if (ui5Type === "Button" && children.length === 1 && children[0].ui5Type === "Label") {
    text = children[0].text;
    children = [];
  }
  return { ui5Type, name: node.name || "", text, layout: node.layoutMode || null, children };
}

async function requestPreviewURL(xmlCode) {
  const res = await fetch("http://localhost:8000/preview-ui5", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ xml: xmlCode }),
  });

  const result = await res.json();
  return result.url;
}

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'generate-code') {
    const selection = figma.currentPage.selection;
    if (!selection || selection.length === 0) {
      figma.ui.postMessage({ type: 'code-generated', code: 'Keine Elemente ausgewählt.' });
      return;
    }

    const traversed = selection.map(traverse).filter(Boolean);
    const mapped = traversed.map(mapTreeToUI5).filter(Boolean);

    try {
      const result = await sendToBackend(mapped);

      let previewURL = null;

      if (result.xml) {
        try {
          previewURL = await requestPreviewURL(result.xml);
        } catch (err) {
          console.warn("Vorschaufehler:", err.message);
        }
      }

      figma.ui.postMessage({
        type: 'code-generated',
        code: result.xml || "Fehler: Kein Code erhalten.",
        metadata: result.metadata || null,
        previewUrl: previewURL
      });
    } catch (e) {
      figma.ui.postMessage({ type: 'code-generated', code: `Backend-Fehler: ${e.message}` });
    }
  }
};