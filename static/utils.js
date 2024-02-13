function GroupListTwoByTwo(list) {
    return list.reduce((acc, e, i) => {
        if (i % 2 === 0) {
            acc.push(i < list.length-1 ? [e, list[i + 1]] : [e]);
        }
        return acc;
    }, []);
}