const gridContainer = document.getElementById("container");

const blocks = {};


function DefaultStruct() {
    gridContainer.innerHTML = `<div class="item" id="header"><h1>Remote Kerbal Commander</h1><div id="info"><span>PING: <span id="ping">--</span></span><span>IP: ${document.domain}</span></div></div>`;
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
    
        gridContainer.appendChild(element);
    }
}

function UpdateValues(data) {
    //blocks[data.ke].setValues(data.params)

    for (const key in data) {
        for (let i = 0; i < data[key].length; i++) {
            //console.log(blocks[key][i])
            blocks[key][i].setValues(data[key][i])
        }
    }
}