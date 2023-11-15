const express = require('express');
const app = express();

const port = process.env.PORT;

app.listen(port, () => console.log(`Listening on port ${port}.`));

app.get('/', (req, res) => {
    const output = Object.assign(
        { timestamp: Date.now() },
        req.headers,
    );
    console.log(output);
    res.send(`Accessed from port ${port}.\n`);
});
