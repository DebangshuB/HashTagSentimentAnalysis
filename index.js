const express = require('express');
const app = express();

//Import PythonShell module.
const { PythonShell } = require('python-shell');

app.use(express.static('static'));
app.use(express.json()); //Used to parse JSON bodies
app.use(express.urlencoded()); //Parse URL-encoded bodies

app.get("/api/:str", (req, res, next) => {

    console.log("Server Recieved Request....")

    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // Get print results in real-time
        scriptPath: './static/', // If you are having python_test.py script in same folder, then it's optional.
        args: [req.params.str, 100] // An argument which can be accessed in the script using sys.argv[1]
    };


    PythonShell.run('pipeline.py', options, function(err, result) {
        if (err) throw err;

        result = result.toString();
        result = result.split(",");
        result = result.map(parseFloat);

        result.pop();
        console.log(result);
        res.send({ 'data': result.toString() })
    });
});

app.get("/", (req, res) => {
    res.sendFile('index.html');
});

const PORT = 8000;

app.listen(PORT, () => console.log(`Server connected to ${PORT}`));