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
export function onScreenLog(message, type = "log") {
    const time = new Date().toLocaleTimeString();

    const $entry = $("<div>", {
        class: `log-entry log-${type}`
    });

    const formattedMessage = formatMessage(message);

    $entry.html(`
        <span class="log-time">[${time}]</span>
        ${formattedMessage}
    `);

    $consoleBody.append($entry);

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