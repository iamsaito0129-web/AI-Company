// Premium Dashboard Mock Data & Logic
document.addEventListener('DOMContentLoaded', () => {
    updateDate();
    initCharts();
    loadAssets();
    updateKPIs();
});

function updateDate() {
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
    document.getElementById('current-date').textContent = now.toLocaleDateString('ja-JP', options);
}

function updateKPIs() {
    document.getElementById('net-worth-val').textContent = "¥3,450,200";
    document.getElementById('monthly-income-val').textContent = "¥284,000";
    document.getElementById('monthly-spending-val').textContent = "¥128,450";
}

function initCharts() {
    // Spending Pie Chart
    const ctxSpending = document.getElementById('spendingChart').getContext('2d');
    new Chart(ctxSpending, {
        type: 'doughnut',
        data: {
            labels: ['食費', '固定費', '交通費', '教育費', '雑費', '立替'],
            datasets: [{
                data: [35000, 48000, 12000, 15000, 10000, 8450],
                backgroundColor: [
                    '#9d50bb', '#6e7ff3', '#00d2ff', '#00ff88', '#f8e71c', '#ff4b2b'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#a0a0c0', font: { family: 'Noto Sans JP' } }
                }
            }
        }
    });

    // Trend Bar Chart
    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    new Chart(ctxTrend, {
        type: 'bar',
        data: {
            labels: ['1月', '2月', '3月'],
            datasets: [
                {
                    label: '収入',
                    data: [250000, 265000, 284000],
                    backgroundColor: '#6e7ff3',
                    borderRadius: 8
                },
                {
                    label: '支出',
                    data: [140000, 135000, 128450],
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#a0a0c0' } },
                x: { grid: { display: false }, ticks: { color: '#a0a0c0' } }
            },
            plugins: {
                legend: { labels: { color: '#a0a0c0' } }
            }
        }
    });
}

function loadAssets() {
    const assets = [
        { name: '三菱UFJ銀行', amount: 1250000, note: 'メイン口座' },
        { name: '楽天銀行', amount: 840000, note: '貯蓄用' },
        { name: 'PayPay', amount: 12400, note: '生活費' },
        { name: '交通系IC (Suica)', amount: 3500, note: '移動' },
        { name: '現金', amount: 45000, note: '財布内' }
    ];

    const list = document.getElementById('assets-list');
    list.innerHTML = assets.map(a => `
        <div class="asset-item">
            <div class="asset-info">
                <h4>${a.name}</h4>
                <p>${a.note}</p>
            </div>
            <div class="asset-amount">¥${a.amount.toLocaleString()}</div>
        </div>
    `).join('');
}

function calculateMabuchi() {
    const koma = document.getElementById('koma-count').value;
    const base = 2500; // 仮のコマ単価
    const total = koma * base;
    
    const resultDiv = document.getElementById('mabuchi-result');
    resultDiv.style.opacity = 0;
    setTimeout(() => {
        resultDiv.innerHTML = `見込み月収: ¥${total.toLocaleString()}`;
        resultDiv.style.opacity = 1;
        resultDiv.style.transition = 'opacity 0.5s';
    }, 100);
}
