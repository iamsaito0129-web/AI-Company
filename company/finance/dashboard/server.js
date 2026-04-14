const http = require('http');
const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, '../data/master/finance_master.json');

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204); res.end(); return;
    }

    if (req.url === '/api/data' && req.method === 'GET') {
        try {
            const data = fs.readFileSync(DB_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data);
        } catch (e) {
            res.writeHead(500); res.end(JSON.stringify({ error: e.message }));
        }
    } else if (req.url === '/api/save' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                fs.writeFileSync(DB_FILE, body, 'utf8');
                res.writeHead(200); res.end(JSON.stringify({ success: true }));
            } catch (e) {
                res.writeHead(500); res.end(JSON.stringify({ error: e.message }));
            }
        });
    } else {
        let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
        if (fs.existsSync(filePath) && fs.lstatSync(filePath).isFile()) {
            const ext = path.extname(filePath);
            const contentType = ext === '.html' ? 'text/html' : (ext === '.js' ? 'text/javascript' : (ext === '.css' ? 'text/css' : 'text/plain'));
            res.writeHead(200, { 'Content-Type': contentType });
            fs.createReadStream(filePath).pipe(res);
        } else {
            res.writeHead(404); res.end('Not Found');
        }
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(Server running at http://localhost:);
});
