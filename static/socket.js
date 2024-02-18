// ================= WEBSOCKET =================

const socket = io({autoConnect: false});

socket.on("connect", () => {
    console.log("CONNECTED");
    ClearError();
});

socket.on("setup", msg => {
    DefaultStruct();
    CreateStructs(JSON.parse(msg), socket);
});

socket.on("module-error", reason => {
    ShowError(reason, 0);
});

socket.on("disconnect", reason => {
    ShowError("WebSocket disconnected", 0);
    console.log("DISCONNECTED");
});

socket.connect();