// ================= WEBSOCKET =================

const socket = io({autoConnect: false});

socket.on("connect", () => {
    console.log("CONNECTED");
});

socket.once("setup", msg => {
    DefaultStruct(); // Clear errors
    CreateStructs(JSON.parse(msg), socket);
});

socket.once("lost-signal", reason => {
    ShowError(reason, 0);
    console.log("SIGNAL LOST!");
});

socket.on("disconnect", reason => {
    ShowError("WebSocket disconnected", 0);
    console.log("DISCONNECTED");
});

socket.connect();