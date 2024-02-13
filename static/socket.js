// ================= WEBSOCKET =================

const socket = io({autoConnect: false});

socket.on("connect", () => {
    console.log("CONNECTED");
});

socket.once("setup", msg => {
    DefaultStruct();
    CreateStructs(JSON.parse(msg), socket);
});

socket.once("lost-signal", msg => {
    console.log("SIGNAL LOST!!!");
    console.log(JSON.parse(msg));
});

socket.on("disconnect", reason => {
    console.log("Events:", socket._callbacks);
});

socket.connect();