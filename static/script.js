const grid_container = document.getElementById("container");

const blocks = {};

function ClearError() {
    document.getElementById("errors").innerHTML = "";
}

function ShowError(message, timeout=0) {
    document.getElementById("errors").innerHTML = `<div><h1>ERROR!</h1><span>${message}</span></div>`;

    if (timeout !== 0) setTimeout(ClearError, timeout);
}

function DefaultStruct() {
    grid_container.innerHTML = `<div class="item" id="header"><h1>Remote Kerbal Commander</h1><p>PING: <span id="ping">--</span></p><div id="errors"></div></div>`;
}

function CreateStructs(data, socket) {
    for (const module in data) {
        blocks[module] = [];
    }


    for (const name in data.params) {
        let fields = data.params[name];
        blocks.params.push(new BlockParams(name, socket, fields));
    }

    for (const cam_id in data.camera) {
        blocks.camera.push(new BlockCamera(cam_id, socket));
    }


    all_blocks = [];
    for(const e in blocks) {
        for (const x of blocks[e])
            all_blocks.push(x);
    }

    for (let row of GroupListTwoByTwo(all_blocks)) {
        let element = row[0].element;
    
        if (row.length == 2) {
            let div = document.createElement("div");
            div.className = "two-columns";
    
            for (let block of row) {
                div.appendChild(block.element);
            }
    
            element = div;
        }
    
        grid_container.appendChild(element);
    }

    // PONG handler
    socket.on("pong", msg => {
        socket.emit("pong", msg);
    });
    
    // PING handler
    let ping_element = document.getElementById("ping");
    socket.on("ping", ping => {
        ping_element.innerText = `${ping}ms`;
    });
}

function UpdateValues(data) {
    for (const key in data) {
        for (let i = 0; i < data[key].length; i++) {
            blocks[key][i].setValues(data[key][i]);
        }
    }
}