/**
 * Data Migration Script: finance_db.json -> Firebase RTDB
 * No external dependencies required.
 */

const fs = require('fs');
const https = require('https');
const path = require('path');

const DB_FILE = path.join(__dirname, '../data/finance_db.json');
const PROJECT_ID = 'oku-jissenn';
const USER_ID = 'saito';

// Helper to parse "2026年4月15日" to { year: "2026", month: "04", date: "2026-04-15" }
function parseDate(str) {
    const match = str.match(/(\d+)年(\d+)月(\d+)日/);
    if (!match) return null;
    const y = match[1];
    const m = match[2].padStart(2, '0');
    const d = match[3].padStart(2, '0');
    return { year: y, month: m, full: `${y}-${m}-${d}` };
}

async function migrate() {
    console.log('Reading database file...');
    const raw = fs.readFileSync(DB_FILE, 'utf8');
    const db = JSON.parse(raw);

    const firebaseData = {
        history: { [USER_ID]: {} },
        users: {
            [USER_ID]: {
                assets: { summary: { total: 0, last_updated: Date.now() } }
            }
        }
    };

    let totalIncome = 0;
    let totalExpense = 0;

    // Process Expenditure
    console.log('Processing expenditures...');
    (db.expenditure || []).forEach((item, index) => {
        const dateInfo = parseDate(item.支払日);
        if (!dateInfo) return;

        const { year, month, full } = dateInfo;
        if (!firebaseData.history[USER_ID][year]) firebaseData.history[USER_ID][year] = {};
        if (!firebaseData.history[USER_ID][year][month]) firebaseData.history[USER_ID][year][month] = { records: {} };

        const id = `exp_${index}`;
        firebaseData.history[USER_ID][year][month].records[id] = {
            amount: Number(item.金額),
            category: item.カテゴリー,
            date: full,
            type: 'expense',
            memo: item.備考 || '',
            項目名: item.項目名
        };
        totalExpense += Number(item.金額);
    });

    // Process Income
    console.log('Processing income...');
    (db.income || []).forEach((item, index) => {
        const dateInfo = parseDate(item.支払日);
        if (!dateInfo) return;

        const { year, month, full } = dateInfo;
        if (!firebaseData.history[USER_ID][year]) firebaseData.history[USER_ID][year] = {};
        if (!firebaseData.history[USER_ID][year][month]) firebaseData.history[USER_ID][year][month] = { records: {} };

        const id = `inc_${index}`;
        firebaseData.history[USER_ID][year][month].records[id] = {
            amount: Number(item.金額),
            category: item.カテゴリー,
            date: full,
            type: 'income',
            memo: item.備考 || '',
            項目名: item.項目名
        };
        totalIncome += Number(item.金額);
    });

    firebaseData.users[USER_ID].assets.summary.total = totalIncome - totalExpense;

    console.log(`Summary: Income ¥${totalIncome}, Expense ¥${totalExpense}, Balance ¥${totalIncome - totalExpense}`);
    
    // Upload via REST API
    const url = `https://${PROJECT_ID}-default-rtdb.firebaseio.com/.json`;
    console.log(`Uploading to ${url}...`);

    const payload = JSON.stringify(firebaseData);
    
    const options = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        }
    };

    const req = https.request(url, options, (res) => {
        console.log(`STATUS: ${res.statusCode}`);
        res.on('data', (d) => process.stdout.write(d));
        res.on('end', () => {
            console.log('\nMigration Complete!');
        });
    });

    req.on('error', (e) => {
        console.error(`Problem with request: ${e.message}`);
    });

    req.write(payload);
    req.end();
}

migrate();
