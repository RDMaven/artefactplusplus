import { onScreenLog } from './log.js';

// Configure WebSocket connection.
const clientID = 0 // TODO (WARNING) : SPECIAL ID FOR THE INTERFACE
const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
const wsAdress = `${wsProtocol}//${window.location.host}/ws/${clientID}`;

export var MAPS = null;

onScreenLog(
    `WebSocket configuration :
<pre> - Host        : ${window.location.host}
 - Client ID   : ${clientID}
 - WS Protocol : ${wsProtocol}</pre>`);

export const ws = new WebSocket(wsAdress);
// ------------------------------

// Basic WS functions
ws.onopen = () => onScreenLog("✅ Connected to server", "success");
ws.onclose = () => onScreenLog(" 👋 Disconected");
ws.onerror = (err) => onScreenLog("❌ WebSocket error:", err, "error");
ws.onmessage = (event) => {

    const packet = JSON.parse(event.data);

    switch (packet.type) {
        case "message": {
            const messages = packet.data?.message ?? "";
            onScreenLog(messages, "server");
            break;
        }

        case "maps_list": {
            MAPS = packet.data ?? "";
            onScreenLog("Received maps from server.", "server");
            break;
        }
        default:
            onScreenLog(`Raw : ${event.data}`, "server");
            break;
    }
};
// ws.readyState


/* THIS COMMUNICATION IS WEB INTERFACE -> PYTHON SERVER. 
SENDING MESSAGES FROM THE INTERFACE IS ONLY TO :
- Joystick control
- Change the mode
- Emergency stop
So, three types : 'mode', 'move', 'stop'
*/

function getTimestamp() {
    return Date.now() / 1000; // seconds with decimals
}

// Turn arguments into dict type.
const buildMoveMsg = (x, y) => { return { x, y } };
const buildParamMsg = (parameter_name, value) => { return { parameter_name, value } };
const buildStopMsg = (stop) => { return { stop } };
const buildCartoInitMsg = (map_name, x0, y0) => {return {map_name, x0, y0}};
const buildTraqueInitMsg = () => {return {}};

// Classify the builder function for the different types
const messageBuilders = {
    "move": buildMoveMsg,
    "set_parameter": buildParamMsg,
    "move_cam": buildMoveMsg,
    "carto_init": buildCartoInitMsg,
    "traque_init": buildTraqueInitMsg
}

// Main message builder function
function buildWSMessage(type, ...args) {
    const builder = messageBuilders[type];
    if (!builder) {
        throw new Error(`Unknown WS message type: ${type}`);
    }

    return {
        type,
        from: clientID,
        for: currentRobot,
        timestamp: getTimestamp(),
        data: builder(...args)
    };
}

// WS message sender function
export function sendWSMessage(type, ...args) {
    if (ws.readyState === WebSocket.OPEN) {
        const jsonMessage = buildWSMessage(type, ...args);
        // console.log(jsonMessage);

        // Cas de message a destination du server
        if ((type == "set_parameter" && (jsonMessage["data"]["parameter_name"] == "mode_capture" ))) {
            jsonMessage["for"] = -1;
        }
        ws.send(JSON.stringify(jsonMessage));
    } else if (ws.readyState !== WebSocket.CONNECTING) {
        onScreenLog(`Issue with WS Connection : wsState=${ws.readyState}`);
    }
}



// TODO : receive data, like the position to place the robot on the map (big flemme)
// export function receiveWSMessage(message) {
//     const data = JSON.parse(message);
//     onScreenLog(data)
// }