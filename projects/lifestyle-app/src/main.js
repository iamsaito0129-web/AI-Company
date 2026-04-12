import './style.css'
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// Sample Data (Actually would be parsed from ../.company/lifestyle/ledgers/2026-03.md)
const marchData = {
  summary: {
    income: 250000,
    expense: 185400,
    savings: 64600,
    totalAssets: 377600
  },
  categories: {
    '固定費': 86600,
    '食費': 45000,
    '交際費': 12000,
    '趣味': 25000,
    '美容・服飾': 16800
  },
  transactions: [
    { date: '2026-03-01', item: '家賃', category: '固定費', method: '振込', amount: 75000 },
    { date: '2026-03-05', item: 'ドコモ・ネット', category: '固定費', method: 'カード', amount: 8400 },
    { date: '2026-03-10', item: 'スーパー買い出し', category: '食費', method: 'PayPay', amount: 5200 },
    { date: '2026-03-12', item: '昼食', category: '食費', method: '現金', amount: 800 },
    { date: '2026-03-15', item: '友人との会食', category: '交際費', method: '現金', amount: 4000 },
    { date: '2026-03-18', item: 'サブスク', category: '固定費', method: 'カード', amount: 3200 },
    { date: '2026-03-20', item: 'PC周辺機器', category: '趣味', method: 'カード', amount: 12400 },
    { date: '2026-03-22', item: '書籍', category: '趣味', method: 'PayPay', amount: 3500 },
  ]
};

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
  renderCharts();
  renderTransactions();
});

function renderCharts() {
  // Line Chart for Spending Trend
  const ctxLine = document.getElementById('spendingChart').getContext('2d');
  new Chart(ctxLine, {
    type: 'line',
    data: {
      labels: ['1w', '2w', '3w', '4w'],
      datasets: [{
        label: '支出推移',
        data: [45000, 75000, 115000, 185400],
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
        x: { grid: { display : false }, ticks: { color: '#94a3b8' } }
      }
    }
  });

  // Pie Chart for Categories
  const ctxPie = document.getElementById('categoryChart').getContext('2d');
  new Chart(ctxPie, {
    type: 'doughnut',
    data: {
      labels: Object.keys(marchData.categories),
      datasets: [{
        data: Object.values(marchData.categories),
        backgroundColor: [
          '#6366f1',
          '#ec4899',
          '#f59e0b',
          '#10b981',
          '#8b5cf6'
        ],
        borderWidth: 0,
        hoverOffset: 15
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#94a3b8', font: { size: 10 }, padding: 20 }
        }
      },
      cutout: '70%'
    }
  });
}

function renderTransactions() {
  const listElement = document.getElementById('transactionList');
  listElement.innerHTML = marchData.transactions.map(t => `
    <tr>
      <td style="color: var(--text-muted); font-size: 0.85rem;">${t.date.split('-').slice(1).join('/')}</td>
      <td style="font-weight: 500;">${t.item}</td>
      <td><span class="category-tag">${t.category}</span></td>
      <td style="color: var(--text-muted); font-size: 0.9rem;">${t.method}</td>
      <td style="text-align: right; font-weight: 700;">¥${t.amount.toLocaleString()}</td>
    </tr>
  `).join('');
}
