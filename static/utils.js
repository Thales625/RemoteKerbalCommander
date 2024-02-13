/*
function GroupListTwoByTwo(list) {
return list.reduce((acc, e, i) => {
if (i % 2 === 0) {
acc.push(i < list.length-1 ? [e, list[i + 1]] : [e]);
}
return acc;
}, []);
}
*/

function IsCamera(block) { return block.type == "camera" }
    
function SortByCamera(list) {
    list.sort((a, b) => IsCamera(b) - IsCamera(a));
    return list.reverse();
}

/*

function GroupListTwoByTwo(list) {
    let result = [];
    let aux = [];

    //list = SortByCamera(list);

    console.log(list)

    for (let i = 0; i < list.length; i++) {
        const value = list[i];

        if (IsCamera(value)) {
            if (aux.length > 0) {
                result.push(aux);
                aux = [];
            }

            result.push([value]);

            continue;
        }

        aux.push(value);

        if (aux.length === 2) {
            result.push(aux);
            aux = [];
        }
    }

    console.log(result)

    return result;
}

*/

function SplitList(list) {
    const a = [];
    const b = [];

    for (const value of list) {
        if (IsCamera(value)) {
            a.push(value);
            continue;
        }
            
        b.push(value);
    }

    return { a, b };
}

function TwoByTwo(list) {
    let result = [];
    let aux = [];

    for (const value of list) {
        aux.push(value)
        
        if (aux.length >= 2) {
            result.push(aux)
            aux = [];
            continue
        }
    }

    if (aux.length > 0) result.push(aux);

    return result;
}

function GroupListTwoByTwo(list) {
    const { a, b } = SplitList(list);

    return TwoByTwo(b).concat(TwoByTwo(a))
}