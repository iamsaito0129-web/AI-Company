/**
 * AI-Company Financial Dashboard v2
 * Focus: Behavioral Economics, Safe-to-Spend, Premium UX
 */

let state = {
    transactions: [],
    status: {
        monthly_budgets: {},
        snapshots: []
    },
    act: { balance: 0 }
};

let chartInstance = null;

const init = async () => {
    console.log("Initializing Financial Engine...");
    await fetchData();
    renderAll();
};

const fetchData = async () => {
    try {
        // 開発フェーズではモックデータを優先し、API実装後に切り替え
        const res = await fetch('/api/data');
        const rawData = await res.json();
        
        // データの互換性レイヤー (v1 -> v2)
        // 以前の finance_master.json が配列形式の場合
        if (Array.isArray(rawData)) {
            const latest = rawData[rawData.length - 1] || {};
            state.status.snapshots = rawData.map(d => ({
                month: d.date.substring(0, 7),
                actual_assets: {
                    bank_main: d.bank || 0,
                    paypay: d.paypay || 0
                }
            }));
            // 仮の予算設定
            state.status.monthly_budgets["2026-04"] = { budget_limit: 100000 };
        }
    } catch (e) {
        console.error("Fetch failed, using defaults:", e);
    }
};

const calculateSafeToSpend = () => {
    const currentMonth = "2026-04"; // TODO: 動的取得
    const budget = state.status.monthly_budgets[currentMonth]?.budget_limit || 0;
    
    // 今月の支出合計を計算 (Mock)
    const spentThisMonth = 34200; 
    
    return budget - spentThisMonth;
};

const renderAll = () => {
    renderHero();
    renderStats();
    renderChart();
};

const renderHero = () => {
    const sts = calculateSafeToSpend();
    const amountEl = document.getElementById('safe-to-spend-amount');
    if (amountEl) {
        // アニメーション付きで数値を更新
        animateValue(amountEl, 0, sts, 1000);
    }
};

const renderStats = () => {
    const latest = state.status.snapshots[state.status.snapshots.length - 1] || {};
    const assets = latest.actual_assets || {};
    
    const total = Object.values(assets).reduce((a, b) => a + b, 0);
    
    document.getElementById('stat-networth').innerText = `¥ ${total.toLocaleString()}`;
    document.getElementById('stat-bank').innerText = `¥ ${(assets.bank_main || 0).toLocaleString()}`;
    document.getElementById('stat-digital').innerText = `¥ ${(assets.paypay || 0).toLocaleString()}`;
};

const renderChart = () => {
    const ctx = document.getElementById('mainChart').getContext('2d');
    if (chartInstance) chartInstance.destroy();
    
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: state.status.snapshots.map(s => s.month),
            datasets: [{
                label: 'Net Worth',
                data: state.status.snapshots.map(s => 
                    Object.values(s.actual_assets).reduce((a, b) => a + b, 0)
                ),
                borderColor: '#8b5cf6',
                borderWidth: 3,
                pointBackgroundColor: '#8b5cf6',
                pointBorderColor: 'rgba(255,255,255,0.5)',
                pointRadius: 5,
                tension: 0.4,
                fill: true,
                backgroundColor: (context) => {
                    const chart = context.chart;
                    const {ctx, chartArea} = chart;
                    if (!chartArea) return null;
                    const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                    gradient.addColorStop(0, 'rgba(139, 92, 246, 0.2)');
                    gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');
                    return gradient;
                }
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
            }
        }
    });
};

// Helpers
const animateValue = (obj, start, end, duration) => {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const val = Math.floor(progress * (end - start) + start);
        obj.innerHTML = `<span class="currency">¥</span>${val.toLocaleString()}`;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
};

window.onload = init;
