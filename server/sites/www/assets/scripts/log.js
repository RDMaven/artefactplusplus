// Console elements
const $consoleElement = $(".console-container");
const $consoleBody = $(".console-body");
const $consoleHeader = $(".console-header");

// Collapse toggle
$consoleHeader.on("click", function () {
    $consoleElement.toggleClass("collapsed");
});

// Clear console
export function consoleClear(readyState) {
    $consoleBody.empty();
    if (readyState != WebSocket.CLOSED) {
       onScreenLog("✅ Connected to server", "success");   
    } else {
        onScreenLog(" ❌ Disconected from server", "error");
    }
}


// Main on-screen logger
/* Features:
- Same consecutive messages are kept into one, with a counter. (ex : [6:24:11 PM] Server: MOVE message recieved from THE INTERFACE. (x110))
- Info, server, and important/error messages are automatically colored.
- JSON messages are formatted.
*/
let lastMessageText = null;
let lastEntry = null;
let lastCount = 1;

export function onScreenLog(message, type = "log") {
    const time = new Date().toLocaleTimeString();
    const formattedMessage = formatMessage(message);

    // If same message AND same type as previous one
    if (message === lastMessageText && lastEntry && lastEntry.data("type") === type) {
        lastCount++;

        // Update existing entry
        lastEntry.find(".log-message").html(`${formattedMessage} (x${lastCount})`);
        return;
    }

    // Reset counter for new message
    lastMessageText = message;
    lastCount = 1;

    const $entry = $("<div>", {
        class: `log-entry log-${type}`
    }).data("type", type);

    $entry.html(`
        <span class="log-time">[${time}]</span>
        <span class="log-message">${formattedMessage}</span>
    `);

    $consoleBody.append($entry);

    // Store reference to this entry
    lastEntry = $entry;

    // Auto scroll
    $consoleBody.scrollTop($consoleBody[0].scrollHeight);
}


// Format object logs
function formatMessage(msg) {
    if (typeof msg === "object") {
        return "<pre>" + JSON.stringify(msg, null, 2) + "</pre>";
    }
    return msg;
}