var ping_element = null;
var image_element = null;

var HasStruct = false;

// ================= WEBSOCKET =================

const socket = io({autoConnect: false});

socket.on("connect", () => {
    console.log("CONNECTED")
});

socket.on("setup", msg => {
    let data = JSON.parse(msg);

    DefaultStruct();
    CreateStructs(data);
    
    HasStruct = true;
    
    return
    
    ping_element = document.getElementById("ping");

    // GAMBIARRA
    image_element = document.getElementById("camera");

    image_element.style.width = "300px";
    image_element.style.height = "300px";
});

socket.on("update", msg => {
    if (HasStruct) {
        data = JSON.parse(msg)

        
        // Ping
        //ping = Math.abs(Date.now() - message.sendAt);
        //ping_element.innerText = ping.toFixed(2) + "ms";

        //if (ping > 100) ping_element.style.color = "red";
        //else ping_element.style.color = "green";
        
        UpdateValues(data);

        //UpdateModules(message.modules);
    }
});



socket.on("camera", imageData => {
    //var blob = new Blob([imageData], { type: 'image/png' });
    //image_element.src = URL.createObjectURL(blob);
});



socket.on("disconnect", reason => {
    //ping_element.innerText = "DISCONNECTED";
    //ping_element.style.color = "red";
});


socket.connect()