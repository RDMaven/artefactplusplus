const socket = new WebSocket("/ws");     //INSERER LIEN SERVEUR


socket.onopen = () => {
    console.log("Connected to server");
    log("Connected to server")
};

socket.onmessage = (event) => {
    console.log("Server:", event.data);
    log(event.data)
};

socket.onclose = () => {
    console.log("Disconnected");
    log("Disconected")
};

function sendMessage() {
    socket.send("Hello from JS");
}


document.getElementById("arrow-up").addEventListener("click", () => {
    let obj = JSON.stringify({ event: "move", x: 0, y: 1 });
    socket.send(obj);
});

document.getElementById("arrow-down").addEventListener("click", () => {
    let obj = JSON.stringify({ event: "move", x: 0, y: -1 });
    socket.send(obj);
});

document.getElementById("arrow-left").addEventListener("click", () => {
    let obj = JSON.stringify({ event: "move", x: -1, y: 0 });
    socket.send(obj);
});

document.getElementById("arrow-right").addEventListener("click", () => {
    let obj = JSON.stringify({ event: "move", x: 1, y: 0 });
    socket.send(obj);
});

const log_square = document.getElementById("log_square");

function log(message){
    let p_log = document.createElement("p");
    p_log.innerText = '>>> '+message;
    p_log.style.color = "white";
    log_square.prepend(p_log);
    log_square.scrollTop = log_square.scrollHeight;
}