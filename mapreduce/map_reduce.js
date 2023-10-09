const fs = require('fs');

function getMapInput(host) {
    const path = `hosts/${host}/people.csv`;
    return fs.readFileSync(path, 'utf-8');
}

function emitMapResults(host, key, value) {
    const path = `hosts/${host}/results/${key}.txt`;
    fs.appendFileSync(path, `${value}\n`);
}

function getReduceInputs() {
    const fileNames = fs.readdirSync('intermediate', 'utf-8')
    const inputs = {};

    for (const fileName of fileNames) {
        if (fileName == '.gitkeep') {
            continue;
        }

        const key = fileName.split('.')[0];
        const contents = fs.readFileSync(`intermediate/${fileName}`, 'utf-8');

        inputs[key] = contents.split('\n').filter(v => v !== '');
    }

    return inputs;
}

function emitReduceResults(key, value) {
    const path = `result/output.txt`;
    fs.appendFileSync(path, `${key}: ${value}\n`);
}

module.exports.getMapInput = getMapInput;
module.exports.emitMapResults = emitMapResults;
module.exports.getReduceInputs = getReduceInputs;
module.exports.emitReduceResults = emitReduceResults;
