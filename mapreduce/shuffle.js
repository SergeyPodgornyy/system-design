const fs = require('fs');

const HOSTS = process.env.HOSTS.split(',');

for (const host of HOSTS) {
    const fileNames = fs.readdirSync(`hosts/${host}/results`, 'utf-8');

    for (const fileName of fileNames) {
        if (fileName === '.gitkeep') {
            continue;
        }

        const key = fileName.split('.')[0];
        const contents = fs.readFileSync(`hosts/${host}/results/${fileName}`, 'utf-8');

        fs.appendFileSync(`intermediate/${key}.txt`, contents);
    }
}
