const mapReduce = require('./map_reduce');

function reduce(key, values) {
    const count = values.reduce(
        (accumulator, current) => accumulator + parseInt(current),
        0
    );
    mapReduce.emitReduceResults(key, count);
}

const reduceInputs = mapReduce.getReduceInputs();
for (const [num, values] of Object.entries(reduceInputs)) {
    const month = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }[num] || 'invalid';

    reduce(month, values);
}
