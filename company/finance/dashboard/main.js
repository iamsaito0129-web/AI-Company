/**
 * AI-FINANCE Dashboard Core Logic
 * Handles View Switching, Data Fetching, Rendering, and Transaction Entry
 */

const app = {
    state: {
        records: { expenditure: [], income: [], settlement: [] },
        currentView: 'dashboard',
        entryMode: 'income', // 'income' or 'expense'
        currentAmount: '0',
        sidebarVisible: true,
        charts: {}
    },

    async init() {
        console.log('Initializing AI-FINANCE system...');
        this.setupEventListeners();
        this.startClock();
        await this.fetchData();
        this.renderAll();
    },

    startClock() {
        const updateClock = () => {
            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0];
            const clockEl = document.getElementById('system-clock');
            if (clockEl) clockEl.innerText = timeStr;
        };
        setInterval(updateClock, 1000);
        updateClock();
    },

    setupEventListeners() {
        // Hamburger toggle
        document.getElementById('hamburger').addEventListener('click', () => this.toggleSidebar());

        // Sidebar Nav links
        document.querySelectorAll('.nav-link[data-view], .mobile-nav-btn[data-view]').forEach(link => {
            link.addEventListener('click', (e) => {
                const viewId = e.currentTarget.getAttribute('data-view');
                this.switchView(viewId);
            });
        });

        // Entry Mode Toggle
        const typeToggle = document.getElementById('type-toggle');
        if (typeToggle) {
            typeToggle.addEventListener('click', () => {
                this.state.entryMode = this.state.entryMode === 'income' ? 'expense' : 'income';
                typeToggle.classList.toggle('active');
                
                // Update labels opacity
                document.getElementById('label-income').style.opacity = this.state.entryMode === 'income' ? '1' : '0.4';
                document.getElementById('label-expense').style.opacity = this.state.entryMode === 'expense' ? '1' : '0.4';
                
                // Update category options based on mode
                this.updateCategoryOptions();
            });
        }

        // Submit Record
        const submitBtn = document.getElementById('submit-record');
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitRecord());
        }

        // Sync button
        const syncBtn = document.getElementById('sync-btn');
        if (syncBtn) {
            syncBtn.addEventListener('click', async () => {
                await this.fetchData();
                this.renderAll();
                alert('Data synchronized with JSON storage.');
            });
        }
    },

    async fetchData() {
        try {
            const response = await fetch('/api/finance/records');
            const data = await response.json();
            this.state.records = data;
            console.log('Data fetched successfully:', data);
        } catch (err) {
            console.error('Failed to fetch finance records:', err);
        }
    },

    renderAll() {
        this.renderDashboard();
        this.renderHistory();
        this.renderAnalysis();
    },

    renderDashboard() {
        const { expenditure, income } = this.state.records;
        
        // Calculate totals
        const totalIncome = income.reduce((acc, r) => acc + (parseFloat(r.金額) || 0), 0);
        const totalExpense = expenditure.reduce((acc, r) => acc + (parseFloat(r.金額) || 0), 0);
        const balance = totalIncome - totalExpense;

        // Update Dot Matrix
        document.getElementById('total-balance').innerText = `¥${balance.toLocaleString()}`;
        document.getElementById('monthly-income').innerText = `¥${totalIncome.toLocaleString()}`;
        document.getElementById('monthly-expense').innerText = `¥${totalExpense.toLocaleString()}`;

        this.updateCharts();
    },

    updateCharts() {
        const ctx = document.getElementById('assetChart').getContext('2d');
        if (this.state.charts.asset) this.state.charts.asset.destroy();

        // Simple mock trend for visualization
        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        this.state.charts.asset = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Asset Trend',
                    data: [1200000, 1350000, 1280000, 1450000, 1400000, 1550000],
                    borderColor: '#ff3b3b',
                    backgroundColor: 'rgba(255, 59, 59, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#666' } },
                    x: { grid: { display: false }, ticks: { color: '#666' } }
                }
            }
        });
    },

    renderHistory() {
        const container = document.getElementById('history-container');
        if (!container) return;

        // Merge and sort all records
        const all = [
            ...this.state.records.income.map(r => ({ ...r, type: 'INCOME', color: '#00ffaa' })),
            ...this.state.records.expenditure.map(r => ({ ...r, type: 'EXPENSE', color: '#ff3b3b' }))
        ].sort((a, b) => new Date(b.日付) - new Date(a.日付));

        container.innerHTML = all.slice(0, 50).map(r => `
            <div class="history-item">
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.7rem; color: var(--text-dim);">${r.日付}</span>
                    <span style="font-weight: 600;">${r.用途 || r.項目 || 'No Description'}</span>
                </div>
                <div style="text-align: right;">
                    <div style="color: ${r.color}; font-weight: 700;">${r.type === 'EXPENSE' ? '-' : '+'} ¥${(parseFloat(r.金額) || 0).toLocaleString()}</div>
                    <div class="view-subtitle" style="font-size: 0.5rem; opacity: 0.5;">${r.カテゴリ || 'OTHER'}</div>
                </div>
            </div>
        `).join('');
    },

    renderAnalysis() {
        const ctx = document.getElementById('categoryPieChart').getContext('2d');
        if (this.state.charts.pie) this.state.charts.pie.destroy();

        const categories = {};
        this.state.records.expenditure.forEach(r => {
            const cat = r.カテゴリ || 'その他';
            categories[cat] = (categories[cat] || 0) + (parseFloat(r.金額) || 0);
        });

        this.state.charts.pie = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(categories),
                datasets: [{
                    data: Object.values(categories),
                    backgroundColor: ['#ff3b3b', '#00ffaa', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { color: '#aaa', font: { family: 'Space Grotesk' } } }
                }
            }
        });
    },

    switchView(viewId) {
        // Update active class in sidebar/mobile nav
        document.querySelectorAll('.nav-link, .mobile-nav-btn').forEach(el => {
            if (el.getAttribute('data-view') === viewId) el.classList.add('active');
            else el.classList.remove('active');
        });

        // Toggle views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });
        document.getElementById(viewId).classList.add('active');
        
        this.state.currentView = viewId;
        
        // Hide sidebar on mobile after selection
        if (window.innerWidth < 1200) {
            this.toggleSidebar(false);
        }
    },

    toggleSidebar(force) {
        const sidebar = document.getElementById('sidebar');
        const main = document.getElementById('main-content');
        
        if (force !== undefined) this.state.sidebarVisible = force;
        else this.state.sidebarVisible = !this.state.sidebarVisible;

        if (this.state.sidebarVisible) {
            sidebar.classList.remove('hidden');
            main.classList.remove('expanded');
        } else {
            sidebar.classList.add('hidden');
            main.classList.add('expanded');
        }
    },

    keypadInput(val) {
        if (val === 'C') {
            this.state.currentAmount = '0';
        } else {
            if (this.state.currentAmount === '0' && val !== '00') {
                this.state.currentAmount = val;
            } else {
                this.state.currentAmount += val;
            }
        }
        
        // Format with commas
        const formatted = parseInt(this.state.currentAmount).toLocaleString();
        document.getElementById('amount-display').innerText = formatted;
    },

    updateCategoryOptions() {
        const select = document.getElementById('category-select');
        const incomeCats = ['給与', '賞与', '副業', '利息', 'その他'];
        const expenseCats = ['食費', '日用品', '娯楽', '交通費', '住宅', '通信', '光熱費', 'その他'];
        
        const cats = this.state.entryMode === 'income' ? incomeCats : expenseCats;
        select.innerHTML = cats.map(c => `<option value="${c}">${c}</option>`).join('');
    },

    async submitRecord() {
        const amount = parseInt(this.state.currentAmount);
        if (amount <= 0) return alert('Please enter a valid amount.');

        const category = document.getElementById('category-select').value;
        const record = {
            日付: new Date().toISOString().split('T')[0],
            カテゴリ: category,
            金額: amount,
            用途: `${category} (Quick Entry)`
        };

        try {
            const endpoint = this.state.entryMode === 'income' ? '/api/income/add' : '/api/finance/add';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(record)
            });

            if (response.ok) {
                alert('Record saved successfully.');
                this.state.currentAmount = '0';
                document.getElementById('amount-display').innerText = '0';
                await this.fetchData();
                this.renderAll();
                this.switchView('dashboard');
            }
        } catch (err) {
            console.error('Submission failed:', err);
        }
    }
};

// Initialize app on load
window.onload = () => app.init();
