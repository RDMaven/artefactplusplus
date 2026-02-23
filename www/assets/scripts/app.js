

const socket = new WebSocket("/ws");     //INSERER LIEN SERVEUR

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
