
class BlockParams {
    constructor(name, struct_list) {
        this.name = name;

        this.struct_names = struct_list;

        this.element = document.createElement("div");
        this.element.className = "item";

        this.value_elements = []; // list[<span>]

        // Construct
        let div_container = document.createElement("div");
        div_container.innerHTML = `<h2>${this.name}</h2>`;

        for (let struct_name of this.struct_names) {
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

    setValues(list_values) {
        if (list_values.length !== this.value_elements.length) return;

        for (let i = 0; i < list_values.length; i++) {
            if (i < this.value_elements.length) this.value_elements[i].innerText = list_values[i];
        }
    }
}


class BlockCamera {
    constructor(name, struct_list) {
        this.name = name;

        this.struct_names = struct_list;

        this.element = document.createElement("div");
        this.element.className = "item";

        this.value_elements = []; // list[<span>]

        // Construct
        let div_container = document.createElement("div");
        div_container.innerHTML = `<h2>${this.name}</h2>`;

        for (let struct_name of this.struct_names) {
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

    setValues(list_values) {
        if (list_values.length !== this.value_elements.length) return;

        for (let i = 0; i < list_values.length; i++) {
            if (i < this.value_elements.length) this.value_elements[i].innerText = list_values[i];
        }
    }
}