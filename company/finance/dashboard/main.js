/**
 * AI-Company Financial Dashboard v2.5
 * Portal Logic & Three-Point Audit System
 */

let state = {
    view: 'dashboard',
    records: {
        expenditure: [],
        income: [],
        settlement: []
    },
    savedViews: [],
    entryValue: "0",
    currentMonth: "2026-03" // Default, will be updated from data
};

const RecordManager = {
    parseDate(dateStr) {
        if (!dateStr) return null;
        let s = dateStr.toString().trim();
        
        // 1. 2026年4月15日
        let match = s.match(/(\d+)年(\d+)月(\d+)日/);
        if (match) return `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
        
        // 2. 2026/04/15 or 2026/4/5
        match = s.match(/(\d+)\/(\d+)\/(\d+)/);
        if (match) return `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
        
        // 3. 2026-04-15
        match = s.match(/(\d+)-(\d+)-(\d+)/);
        if (match) return `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
        
        return null;
    },

    getMonth(dateStr) {
        const parsed = this.parseDate(dateStr);
        return parsed ? parsed.substring(0, 7) : null;
    },

    getTotalsByMonth(month) {
        const exp = state.records.expenditure
            .filter(r => this.getMonth(r['支払日']) === month)
            .reduce((sum, r) => sum + (Number(r['金額']) || 0), 0);
        
        const inc = state.records.income
            .filter(r => this.getMonth(r['支払日']) === month)
            .reduce((sum, r) => sum + (Number(r['金額']) || 0), 0);
        
        return { expenditure: exp, income: inc };
    },

    getCategoryTrends(month) {
        const months = [month, this.getPrevMonth(month), this.getPrevMonth(this.getPrevMonth(month))];
        const categories = [...new Set(state.records.expenditure.map(r => r['カテゴリー']))];
        
        return categories.map(cat => {
            const data = months.map(m => {
                const filtered = state.records.expenditure.filter(r => r['カテゴリー'] === cat && this.getMonth(r['支払日']) === m);
                return {
                    total: filtered.reduce((sum, r) => sum + (Number(r['金額']) || 0), 0),
                    count: filtered.length
                };
            });
            
            return { 
                category: cat, 
                m0: data[0].total, m0_count: data[0].count,
                m1: data[1].total, m1_count: data[1].count,
                m2: data[2].total, m2_count: data[2].count
            };
        }).filter(item => item.m0 > 0 || item.m1 > 0 || item.m2 > 0)
          .sort((a, b) => b.m0 - a.m0);
    },

    getPrevMonth(month) {
        const [y, m] = month.split('-').map(Number);
        if (m === 1) return `${y - 1}-12`;
        return `${y}-${(m - 1).toString().padStart(2, '0')}`;
    }
};

// --- Initialization ---
const init = async () => {
    console.log("Initializing Financial Engine v2.5...");
    setupEventListeners();
    await fetchFinanceRecords();
    
    // Determine current month from latest records
    let allDates = [
        ...state.records.expenditure.map(r => RecordManager.parseDate(r['支払日'])),
        ...state.records.income.map(r => RecordManager.parseDate(r['支払日'])),
        ...state.records.settlement.map(r => RecordManager.parseDate(r['決算日']))
    ].filter(d => d);

    if (allDates.length > 0) {
        allDates.sort().reverse();
        state.currentMonth = allDates[0].substring(0, 7);
    } else {
        const now = new Date();
        state.currentMonth = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}`;
    }

    console.log("Current state month:", state.currentMonth);
    renderAll();
};

const setupEventListeners = () => {
    // View switching (handles by global switchView)
    window.switchView = (viewId) => {
        console.log("Switching view to:", viewId);
        state.view = viewId;
        
        // Hide all views
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        
        // Show target view
        const target = document.getElementById(`view-${viewId}`);
        if (target) {
            target.classList.add('active');
            window.scrollTo(0, 0); // Reset scroll position
        } else {
            console.error(`View not found: view-${viewId}`);
        }
        
        // Update sidebar links
        document.querySelectorAll('.nav-link').forEach(l => {
            l.classList.toggle('active', l.getAttribute('data-view') === viewId);
        });

        // Update bottom nav active state
        document.querySelectorAll('.quick-actions .action-btn').forEach(btn => {
            const viewAttr = btn.getAttribute('data-view');
            btn.classList.toggle('active', viewAttr === viewId);
        });
        
        renderAll();
    };

    // Global Search
    const searchInput = document.getElementById('global-search');
    searchInput?.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (query) {
            switchView('history');
            filterHistory(query);
        }
    });

    // Load saved views
    state.savedViews = JSON.parse(localStorage.getItem('finance_saved_views') || '[]');
    renderSavedViews();

    // Salary Modal
    const salaryModal = document.getElementById('salary-modal');
    const closeBtn = document.querySelector('.close-btn');
    document.getElementById('btn-salary-portal')?.addEventListener('click', () => salaryModal.style.display = 'block');
    document.getElementById('btn-salary')?.addEventListener('click', () => salaryModal.style.display = 'block');
    closeBtn.onclick = () => salaryModal.style.display = 'none';
    window.onclick = (e) => { if (e.target == salaryModal) salaryModal.style.display = 'none'; };

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('global-search')?.focus();
        }
    });

    // Nav Links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            const viewId = link.getAttribute('data-view');
            switchView(viewId);
        });
    });
};

const fetchFinanceRecords = async () => {
    try {
        console.log("Fetching /api/finance/records...");
        const res = await fetch('/api/finance/records');
        console.log("Response status:", res.status);
        if (!res.ok) {
            const text = await res.text();
            console.error("API Error Response:", text);
            return;
        }
        state.records = await res.json();
        console.log("Records loaded:", state.records);
    } catch (e) {
        console.error("Fetch failed:", e);
    }
};

const filterHistory = (query) => {
    const filtered = state.records.expenditure.filter(r => 
        (r['項目名'] && r['項目名'].toLowerCase().includes(query)) || 
        (r['カテゴリー'] && r['カテゴリー'].toLowerCase().includes(query)) ||
        (r['備考'] && r['備考'].toLowerCase().includes(query))
    );
    renderHistoryList(filtered);
};

const renderHistoryList = (data) => {
    const container = document.getElementById('history-list');
    if (!container) return;
    container.innerHTML = '';
    let lastDate = '';
    
    data.slice(0, 50).forEach(tx => {
        const date = tx['支払日'];
        if (date !== lastDate) {
            const header = document.createElement('div');
            header.className = 'history-date-header';
            header.textContent = date;
            container.appendChild(header);
            lastDate = date;
        }
        
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div>
                <div>${tx['項目名']}</div>
                <div class="dim text-xs">${tx['カテゴリー']} • ${tx['備考'] || ''}</div>
            </div>
            <div class="amount-neg">-¥${Number(tx['金額']).toLocaleString()}</div>
        `;
        container.appendChild(item);
    });
};

const renderSavedViews = () => {
    const container = document.querySelector('.matrix-card.flex-1 .space-y-2');
    if (!container) return;
    container.innerHTML = '';
    state.savedViews.forEach((view, idx) => {
        const div = document.createElement('div');
        div.className = 'service-item';
        div.onclick = () => {
            switchView('history');
            filterHistory(view.query);
        };
        div.innerHTML = `
            <div class="service-icon"><i class="fas fa-star"></i></div>
            <div>
                <div class="text-sm font-medium">${view.name}</div>
                <div class="text-xs dim">Query: ${view.query}</div>
            </div>
        `;
        container.appendChild(div);
    });
};

window.saveCurrentView = () => {
    const query = document.getElementById('global-search').value;
    if (!query) return alert("Search something first!");
    const name = prompt("View name:", query);
    if (name) {
        state.savedViews.push({ name, query });
        localStorage.setItem('finance_saved_views', JSON.stringify(state.savedViews));
        renderSavedViews();
    }
};

// Removed duplicate switchView

// --- Rendering ---
const renderAll = () => {
    console.log("Rendering all for view:", state.view);
    if (state.view === 'dashboard') renderPortal();
    else if (state.view === 'audit') renderAudit();
    else if (state.view === 'history') renderHistory();
    else if (state.view === 'analysis') renderAnalysis();
    else if (state.view === 'entry') { /* Entry handled by UI */ }
};

const renderPortal = () => {
    const totals = RecordManager.getTotalsByMonth(state.currentMonth);
    const prevTotals = RecordManager.getTotalsByMonth(RecordManager.getPrevMonth(state.currentMonth));
    
    // Net Income
    const net = totals.income - totals.expenditure;
    const prevNet = prevTotals.income - prevTotals.expenditure;
    const diffNet = net - prevNet;
    
    document.getElementById('metric-net-income').textContent = `¥${net.toLocaleString()}`;
    const trendEl = document.getElementById('trend-net-income');
    trendEl.textContent = `${diffNet >= 0 ? '↑' : '↓'} ¥${Math.abs(diffNet).toLocaleString()} vs last month`;
    trendEl.className = `text-xs mt-2 ${diffNet >= 0 ? 'trend-pos' : 'trend-neg'}`;

    // Allowance (Static for now, should be from a config)
    const allowance = 150000 - totals.expenditure; 
    document.getElementById('metric-allowance').textContent = `¥${allowance.toLocaleString()}`;
    const ratio = Math.min(100, Math.max(0, (totals.expenditure / 150000) * 100));
    document.querySelector('.progress-fill').style.width = `${ratio}%`;
    document.getElementById('metric-budget-ratio').textContent = `${Math.round(ratio)}%`;

    // Recent Activity (Portal list)
    const recentList = document.getElementById('portal-recent-list');
    recentList.innerHTML = '';
    state.records.expenditure.slice(0, 5).forEach(r => {
        const div = document.createElement('div');
        div.className = 'history-item';
        div.innerHTML = `
            <div class="flex items-center gap-3">
                <div class="service-icon"><i class="fas fa-shopping-cart"></i></div>
                <div>
                    <div class="text-sm font-medium">${r['項目名']}</div>
                    <div class="text-xs dim">${r['カテゴリー']} • ${r['支払日']}</div>
                </div>
            </div>
            <div class="amount-neg">-¥${Number(r['金額']).toLocaleString()}</div>
        `;
        recentList.appendChild(div);
    });
};

const renderAudit = () => {
    const month = state.currentMonth;
    const prevMonth = RecordManager.getPrevMonth(month);
    
    const currentSettlement = state.records.settlement.find(s => RecordManager.getMonth(s['決算日']) === month);
    const prevSettlement = state.records.settlement.find(s => RecordManager.getMonth(s['決算日']) === prevMonth);
    
    const totals = RecordManager.getTotalsByMonth(month);
    
    if (currentSettlement && prevSettlement) {
        const prevTotal = Number(prevSettlement['合計金額']) || 0;
        const actualTotal = Number(currentSettlement['合計金額']) || 0;
        const theoryTotal = prevTotal + totals.income - totals.expenditure;
        const diff = actualTotal - theoryTotal;
        
        document.getElementById('audit-theory').textContent = `¥${theoryTotal.toLocaleString()}`;
        document.getElementById('audit-actual').textContent = `¥${actualTotal.toLocaleString()}`;
        document.getElementById('audit-delta').textContent = `¥${diff.toLocaleString()}`;
        document.getElementById('audit-diff').textContent = `¥${diff.toLocaleString()}`;
        
        const statusEl = document.getElementById('audit-status');
        if (Math.abs(diff) < 10) {
            statusEl.textContent = "SYSTEM INTEGRITY SECURED";
            statusEl.className = "text-sm mt-2 trend-pos";
        } else {
            statusEl.textContent = "DISCREPANCY DETECTED / AUDIT REQUIRED";
            statusEl.className = "text-sm mt-2 trend-neg";
        }
    }

    // Category Trends Table
    const trends = RecordManager.getCategoryTrends(month);
    const tbody = document.querySelector('#trend-table tbody');
    tbody.innerHTML = '';
    trends.forEach(t => {
        const tr = document.createElement('tr');
        tr.className = "border-b border-white/5 hover:bg-white/5";
        const trendIcon = t.m0 > t.m1 ? '<span class="trend-neg">↑</span>' : (t.m0 < t.m1 ? '<span class="trend-pos">↓</span>' : '');
        tr.innerHTML = `
            <td class="py-3 font-medium">${t.category}</td>
            <td>¥${t.m0.toLocaleString()} ${trendIcon} <br><span class="dim text-[10px]">${t.m0_count}回</span></td>
            <td class="dim">¥${t.m1.toLocaleString()} <br><span class="text-[10px]">${t.m1_count}回</span></td>
            <td class="dim">¥${t.m2.toLocaleString()} <br><span class="text-[10px]">${t.m2_count}回</span></td>
        `;
        tbody.appendChild(tr);
    });
};

const renderHistory = () => {
    const container = document.getElementById('history-list');
    container.innerHTML = '';
    let lastDate = '';
    
    state.records.expenditure.slice(0, 50).forEach(tx => {
        const date = tx['支払日'];
        if (date !== lastDate) {
            const header = document.createElement('div');
            header.className = 'history-date-header';
            header.textContent = date;
            container.appendChild(header);
            lastDate = date;
        }
        
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div>
                <div>${tx['項目名']}</div>
                <div class="dim text-xs">${tx['カテゴリー']} • ${tx['備考'] || ''}</div>
            </div>
            <div class="amount-neg">-¥${Number(tx['金額']).toLocaleString()}</div>
        `;
        container.appendChild(item);
    });
};

const renderAnalysis = () => {
    // Radar chart for asset distribution
    const ctx = document.getElementById('analysisChart');
    if (!ctx) return;
    
    const latest = state.records.settlement[0];
    if (!latest) return;
    
    const data = [
        Number(latest['銀行口座残高']) || 0,
        Number(latest['paypay残高']) || 0,
        (Number(latest['財布（青）']) || 0) + (Number(latest['財布（黒橙）']) || 0),
        Number(latest['スマホSuica']) || 0,
        Number(latest['引き出しのへそくり']) || 0
    ];

    if (window.analysisChartInstance) window.analysisChartInstance.destroy();
    window.analysisChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Bank', 'PayPay', 'Wallet', 'Suica', 'Secret'],
            datasets: [{
                label: 'Asset Distribution',
                data: data,
                backgroundColor: 'rgba(255, 0, 0, 0.2)',
                borderColor: '#ff0000',
                borderWidth: 2,
                pointBackgroundColor: '#ff0000'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#888', font: { size: 10 } },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
};

// --- Numpad Logic ---
window.pressNum = (num) => {
    if (state.entryValue === "0") state.entryValue = num.toString();
    else state.entryValue += num.toString();
    updateEntryDisplay();
};

window.clearNum = () => {
    state.entryValue = "0";
    updateEntryDisplay();
};

window.submitNum = () => {
    alert(`Entered: ¥${Number(state.entryValue).toLocaleString()}`);
    // In a real app, this would send to server
    clearNum();
};

const updateEntryDisplay = () => {
    document.getElementById('numpad-display').textContent = Number(state.entryValue).toLocaleString();
};

window.onload = init;
