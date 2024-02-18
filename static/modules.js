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

        // SWITCH
        for (let attr in fields.switch) {
            let p = document.createElement("p");

            let switch_element = document.createElement("input");
            switch_element.type = "checkbox";
            switch_element.checked = Boolean(fields.switch[attr]["value"])
            

            let switch_element_display = document.createElement("span");
            switch_element_display.style.color = "green";
            switch_element_display.innerText = switch_element.checked;

            
            socket.on(`update:controller:switch:${attr}`, msg => {
                switch_element_display.innerText = msg;
                switch_element.checked = msg;
                switch_element_display.style.color = "green";
            });
            
            switch_element.onchange = e => {
                socket.emit(`update:controller:switch:${attr}`, e.target.checked);
                switch_element_display.innerText = e.target.checked;
                switch_element_display.style.color = "red";
            };
            
            
            p.innerHTML = `<span class="block-name">${attr}</span>`;
            p.appendChild(switch_element);
            p.appendChild(switch_element_display);
            
            div_container.appendChild(p);
        }

        // SLIDER
        for (let attr in fields.slider) {
            let p = document.createElement("p");

            let interval = fields.slider[attr]["interval"];
            let slider = document.createElement("input");
            slider.type = "range";
            slider.min = interval[0];
            slider.max = interval[1];

            slider.value = Number(fields.slider[attr]["value"]);

            let slider_display = document.createElement("span");
            slider_display.style.color = "green";
            slider_display.innerText = slider.value;

            socket.on(`update:controller:slider:${attr}`, msg => {
                slider_display.innerText = Number(msg);
                slider.value = Number(msg);
                slider_display.style.color = "green";
            });

            slider.onchange = e => {
                socket.emit(`update:controller:slider:${attr}`, e.target.value);
                slider_display.innerText = e.target.value;
                slider_display.style.color = "red";
            };
            
            p.innerHTML = `<span class="block-name">${attr}</span>`;
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