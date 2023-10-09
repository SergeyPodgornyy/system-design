const mapReduce = require('./map_reduce');
const process = require('process');

const HOST = process.env.HOST;

function map(text) {
    const lines = text.split("\n");
    const months = {};

    for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        if (line === '') {
            continue;
        }

        const month = line.split(',')[1].trim().substring(5, 7);
        months[month] = (months[month] || 0) + 1;
    }

    for (let month in months) {
        mapReduce.emitMapResults(HOST, month, months[month]);
    }
}

const mapInput = mapReduce.getMapInput(HOST);
map(mapInput);
