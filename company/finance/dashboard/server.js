const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const DB_FILE = path.join(__dirname, '../data/finance_db.json');
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

    log(`${req.method} ${pathname}`);

    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    // API: GET Records
    if (pathname === '/api/finance/records' && req.method === 'GET') {
        try {
            if (!fs.existsSync(DB_FILE)) {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Database file not found' }));
                return;
            }
            const data = fs.readFileSync(DB_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data);
        } catch (e) {
            log(`API Error: ${e.message}`);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: e.message }));
        }
        return;
    }

    // API: POST Add Record (Supports Expenditure and Income)
    if ((pathname === '/api/finance/add' || pathname === '/api/income/add') && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const input = JSON.parse(body);
                if (!fs.existsSync(DB_FILE)) throw new Error('Database file not found');
                
                const db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
                const isIncome = pathname === '/api/income/add';
                
                const now = new Date();
                const dateStr = input.日付 || `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日`;
                const dateTimeStr = `${dateStr} ${now.getHours()}:${now.getMinutes()}`;
                const settlementDate = `${now.getFullYear()}年${now.getMonth()+1}月${new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate()}日`;

                const newRecord = {
                    "項目名": input.用途 || '新規入力',
                    "支払日": dateStr,
                    "カテゴリー": input.カテゴリ || 'その他',
                    "金額": Number(input.金額),
                    "備考": input.備考 || '',
                    "決算日": settlementDate,
                    "最終更新日時": dateTimeStr,
                    "中間DateBase": 'Dashboard App'
                };

                if (isIncome) {
                    if (!db.income) db.income = [];
                    db.income.unshift(newRecord);
                } else {
                    if (!db.expenditure) db.expenditure = [];
                    db.expenditure.unshift(newRecord);
                }

                fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2), 'utf8');
                log(`Added ${isIncome ? 'Income' : 'Expense'}: ${newRecord["項目名"]} = ¥${newRecord["金額"]}`);
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, record: newRecord }));
            } catch (e) {
                log(`Add Record Error: ${e.message}`);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
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
        res.writeHead(404);
        res.end('Not Found');
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`[AI-FINANCE] Dashboard active at http://localhost:${PORT}`);
});
