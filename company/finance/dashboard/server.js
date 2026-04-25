const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const DB_FILE = path.join(__dirname, '../data/master/finance_master.json');
const LOG_FILE = path.join(__dirname, 'server_debug.log');

function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let pathname = parsedUrl.pathname || '/';
    
    // Normalize: remove trailing slash
    if (pathname !== '/' && pathname.endsWith('/')) {
        pathname = pathname.slice(0, -1);
    }

    log(`${req.method} ${pathname} (Host: ${req.headers.host})`);

    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    // API Routes
    if (pathname.startsWith('/api/finance/records') && req.method === 'GET') {
        log('Handling /api/finance/records');
        try {
            const recordsDir = path.join(__dirname, '../data/records');
            if (!fs.existsSync(recordsDir)) {
                log(`Error: Records dir not found at ${recordsDir}`);
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Records directory not found' }));
                return;
            }

            const files = fs.readdirSync(recordsDir);
            const expFile = files.find(f => f.startsWith('資産管理_支出マスター'));
            const incFile = files.find(f => f.startsWith('資産管理_収入マスター'));
            const setFile = files.find(f => f.startsWith('決済'));

            const parseCSV = (filePath) => {
                const fullPath = path.join(recordsDir, filePath);
                log(`Parsing ${filePath}`);
                const content = fs.readFileSync(fullPath, 'utf8');
                const lines = content.split(/\r?\n/);
                if (lines.length <= 1) return [];
                
                const splitLine = (line) => {
                    const result = [];
                    let cur = '';
                    let inQuote = false;
                    for (let i = 0; i < line.length; i++) {
                        const char = line[i];
                        if (char === '"') {
                            if (inQuote && line[i+1] === '"') { // Double quote
                                cur += '"'; i++;
                            } else {
                                inQuote = !inQuote;
                            }
                        } else if (char === ',' && !inQuote) {
                            result.push(cur.trim());
                            cur = '';
                        } else {
                            cur += char;
                        }
                    }
                    result.push(cur.trim());
                    return result;
                };

                const headers = splitLine(lines[0]);
                return lines.slice(1).filter(l => l.trim()).map(line => {
                    const values = splitLine(line);
                    const obj = {};
                    headers.forEach((header, i) => {
                        let val = values[i] || '';
                        if (val.startsWith('"') && val.endsWith('"')) val = val.substring(1, val.length - 1);
                        if (typeof val === 'string' && (val.includes('￥') || val.includes('¥'))) {
                            val = val.replace(/[￥¥\s,]/g, '');
                            if (val.startsWith('+')) val = val.substring(1);
                        }
                        if (val !== '' && !isNaN(val) && !val.includes('/') && !val.includes('-') && !val.includes('年')) {
                            obj[header] = Number(val);
                        } else {
                            obj[header] = val;
                        }
                    });
                    return obj;
                });
            };

            const data = {
                expenditure: expFile ? parseCSV(expFile) : [],
                income: incFile ? parseCSV(incFile) : [],
                settlement: setFile ? parseCSV(setFile) : []
            };

            log(`Successfully loaded records: Exp=${data.expenditure.length}, Inc=${data.income.length}, Set=${data.settlement.length}`);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(data));
        } catch (e) {
            log(`API Error: ${e.message}`);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: e.message }));
        }
        return;
    }

    if (pathname === '/api/data' && req.method === 'GET') {
        try {
            if (!fs.existsSync(DB_FILE)) {
                fs.mkdirSync(path.dirname(DB_FILE), { recursive: true });
                fs.writeFileSync(DB_FILE, JSON.stringify({ savedViews: [] }), 'utf8');
            }
            const data = fs.readFileSync(DB_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data);
        } catch (e) {
            res.writeHead(500); res.end(JSON.stringify({ error: e.message }));
        }
        return;
    }

    if (pathname === '/api/save' && req.method === 'POST') {
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
        return;
    }

    // Static Files
    let relPath = pathname === '/' ? 'index.html' : pathname;
    if (relPath.startsWith('/')) relPath = relPath.substring(1);
    const filePath = path.join(__dirname, relPath);
    
    if (fs.existsSync(filePath) && fs.lstatSync(filePath).isFile()) {
        const ext = path.extname(filePath);
        const contentType = {
            '.html': 'text/html',
            '.js': 'text/javascript',
            '.css': 'text/css',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.json': 'application/json',
            '.svg': 'image/svg+xml'
        }[ext] || 'text/plain';
        
        res.writeHead(200, { 'Content-Type': contentType });
        fs.createReadStream(filePath).pipe(res);
    } else {
        console.log(`[404] ${pathname} -> looked at ${filePath}`);
        res.writeHead(404);
        res.end('Not Found');
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`Also listening on all interfaces at port ${PORT}`);
});
