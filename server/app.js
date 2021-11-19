const express = require('express');
const cors = require('cors');
const app = express();
app.all('', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "");
    res.header('Access-Control-Allow-Methods: GET, POST');
    res.header("Access-Control-Allow-Headers", "*");
    next();
});
var corsOptions = {
  origin: '*',
}
app.use(cors(corsOptions));
app.get('/', (req, res) => {
  res.json({ message : "Hello from EC2 instance" });
});
app.get('/test', (req, res) => {
  res.json({ message : "test" });
});
const server = app.listen(80, () => {
});
