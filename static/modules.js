class BlockParams {
    constructor(name, socket, struct_list) {
        this.type = "params";

        this.name = name;

        // SOCKET EVENT LISTNER
        socket.on(`update.params:${this.name}`, msg => this.setValues(msg));

        // HTML
        this.element = document.createElement("div");
        this.element.className = "item";

        this.value_elements = []; // list[<span>]
        
        let div_container = document.createElement("div");
        div_container.innerHTML = `<h2>${this.name}</h2>`;

        div_container.style = "width:80%;max-width:300px;";
        
        for (let struct_name of struct_list) {
            let p = document.createElement("p");

            let valueSpan = document.createElement("span");
            valueSpan.className = "block-value";
            valueSpan.innerText = "-";
            this.value_elements.push(valueSpan);

            p.innerHTML = `<span class="block-name">${struct_name}</span>`;
            p.appendChild(valueSpan);
            
            div_container.appendChild(p);
        }

        this.element.appendChild(div_container);
    }

    setValues(message) {
        let list_values = JSON.parse(message);

        if (list_values.length != this.value_elements.length) return;

        for (let i = 0; i < list_values.length; i++) {
            if (i < this.value_elements.length) this.value_elements[i].innerText = list_values[i];
        }
    }
}


class BlockController {
    constructor(fields, socket) {
        this.type = "controller";

        // HTML
        this.element = document.createElement("div");
        this.element.className = "item";

        let div_container = document.createElement("div");
        div_container.innerHTML = `<h2>${this.type}</h2>`;

        div_container.style = "width:80%;max-width:300px;";

        // BUTTON
        if (fields.button) div_container.innerHTML += "<p style='text-decoration:underline'>Buttons</p>"; // REMOVE
        // ...

        // SLIDER
        if (fields.slider) div_container.innerHTML += "<p style='text-decoration:underline'>Sliders</p>"; // REMOVE
        for (let field in fields.slider) {
            let p = document.createElement("p");

            let interval = fields.slider[field]["interval"];

            let slider = document.createElement("input");
            slider.type = "range";
            slider.min = interval[0];
            slider.max = interval[1];

            slider.value = slider.min;

            let slider_display = document.createElement("span");
            slider_display.style.color = "green";
            slider_display.innerText = slider.value;
            // o valor do slider_display pode ser o valor retornado pelo servidor :D

            slider.onchange = e => {
                socket.emit("update:controller:slider", `{"${field}": ${e.target.value}}`);
                slider_display.innerText = e.target.value;
                slider_display.style.color = "red";
            };
            
            socket.on("update:controller:slider", msg => {
                slider_display.innerText = e.target.value;
                slider_display.style.color = "green";
            });

            p.innerHTML = `<span class="block-name">${field}</span>`;
            p.appendChild(slider);
            p.appendChild(slider_display);
            
            div_container.appendChild(p);
        }

        this.element.appendChild(div_container);
    }

    setValues(message) {
        let list_values = JSON.parse(message);

        if (list_values.length != this.value_elements.length) return;

        for (let i = 0; i < list_values.length; i++) {
            if (i < this.value_elements.length) this.value_elements[i].innerText = list_values[i];
        }
    }
}


class BlockCamera {
    constructor(camera_id, socket) {
        this.type = "camera";

        this.id = camera_id;

        // SOCKET
        socket.on(`update.camera:${this.id}`, img => this.setValues(img));

        // HTML
        this.element = document.createElement("div");
        this.element.className = "item";

        // Construct
        let div_container = document.createElement("div");
        div_container.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;"><h2>Camera</h2> <span style="color:gray;margin-left:5px;margin-top:5px;font-size:smaller;">(${this.id})</span></div>`;

        this.image_element = document.createElement("img");
        this.image_element.width = 360;
        this.image_element.height = 360;
        div_container.appendChild(this.image_element);

        this.element.appendChild(div_container);
    }

    setValues(image) {
        var blob = new Blob([image], { type: 'image/png' });
        this.image_element.src = URL.createObjectURL(blob);
    }
}