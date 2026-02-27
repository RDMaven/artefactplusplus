
import { onScreenLog } from './log.js';

// Configure WebSocket connection.
const clientID = Date.now()
const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
const wsAdress = `${wsProtocol}//${window.location.host}/ws/${clientID}`;

onScreenLog(
`WebSocket configuration :
<pre> - Host        : ${window.location.host}
 - Client ID   : ${clientID}
 - WS Protocol : ${wsProtocol}</pre>`);

export const ws = new WebSocket(wsAdress);
// ------------------------------

// Basic WS functions
ws.onopen  = () => onScreenLog("✅ Connected to server", "success");
ws.onclose = () => onScreenLog(" 👋 Disconected");
ws.onmessage = (event) => onScreenLog(`Server sent : ${event.data}`, "server");
ws.onerror   = (err)   => onScreenLog("❌ WebSocket error:", err, "error");
ws.readyState