/**
 * AI-FINANCE: Core Logic (Cloud Native)
 * Premium Asset Management System with Firebase RTDB
 */

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getDatabase, ref, onValue, push, set, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyCgn3msTKtbr7Sm0Jayu0gLu3cRSPnCvn4",
  authDomain: "oku-jissenn.firebaseapp.com",
  projectId: "oku-jissenn",
  storageBucket: "oku-jissenn.firebasestorage.app",
  messagingSenderId: "458948159224",
  appId: "1:458948159224:web:4aa7808fd7179cbb1e3d0d"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const db = getDatabase(firebaseApp);

const app = {
    state: {
        currentView: 'dashboard',
        totalAssets: 0,
        monthlySalary: 200000,
        allocationRatio: 30,
        history: [],
        type: 'expense' // 'expense' or 'income'
    },

    init() {
        this.bindEvents();
        this.updateClock();
        this.setupFirebaseListeners();
        setInterval(() => this.updateClock(), 1000);
    },

    setupFirebaseListeners() {
        const userId = 'saito'; // Static for now, can use Auth later
        
        // Assets Summary Listener
        const assetRef = ref(db, `users/${userId}/assets/summary`);
        onValue(assetRef, (snapshot) => {
            const data = snapshot.val();
            if (data) {
                this.state.totalAssets = data.total || 0;
                this.updateDashboardStats();
            }
        });

        // History Listener
        const historyRef = ref(db, `history/${userId}`);
        onValue(historyRef, (snapshot) => {
            const data = snapshot.val();
            const flattened = [];
            if (data) {
                // Iterate through years/months/records
                Object.keys(data).forEach(year => {
                    Object.keys(data[year]).forEach(month => {
                        const records = data[year][month].records;
                        if (records) {
                            Object.keys(records).forEach(id => {
                                flattened.push({ id, ...records[id] });
                            });
                        }
                    });
                });
                // Sort by date descending
                this.state.history = flattened.sort((a, b) => new Date(b.date) - new Date(a.date));
                this.renderHistory();
                this.renderCharts();
            }
        });
    },

    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-link, .mobile-nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = btn.getAttribute('data-view');
                if (view) this.switchView(view);
            });
        });

        // Salary Slider
        const slider = document.getElementById('allocation-slider');
        if (slider) {
            slider.addEventListener('input', (e) => {
                this.state.allocationRatio = parseInt(e.target.value);
                this.updateAllocationUI();
            });
        }

        // Type Toggle (Expense/Income)
        const toggle = document.getElementById('type-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => {
                this.state.type = this.state.type === 'expense' ? 'income' : 'expense';
                toggle.classList.toggle('active', this.state.type === 'income');
                document.getElementById('label-income').style.opacity = this.state.type === 'income' ? '1' : '0.4';
                document.getElementById('label-expense').style.opacity = this.state.type === 'expense' ? '1' : '0.4';
            });
        }

        // Submit Record
        const submitBtn = document.getElementById('submit-record');
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitToFirebase());
        }

        // Sidebar Toggle
        const hamburger = document.getElementById('hamburger');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (hamburger) {
            hamburger.addEventListener('click', () => this.toggleSidebar());
        }
        if (overlay) {
            overlay.addEventListener('click', () => this.toggleSidebar(false));
        }
    },

    async submitToFirebase() {
        const userId = 'saito';
        const amount = parseInt(this.currentEntryAmount);
        const category = document.getElementById('category-select').value;
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const dateStr = `${year}-${month}-${String(now.getDate()).padStart(2, '0')}`;

        if (amount <= 0) return alert('金額を入力してください');

        const recordRef = ref(db, `history/${userId}/${year}/${month}/records`);
        const newRecord = {
            amount: amount,
            category: category,
            type: this.state.type,
            date: dateStr,
            timestamp: serverTimestamp(),
            source: 'Dashboard App'
        };

        try {
            await push(recordRef, newRecord);
            
            // Update Total Assets (Basic logic: subtract if expense, add if income)
            const summaryRef = ref(db, `users/${userId}/assets/summary`);
            const newTotal = this.state.type === 'expense' 
                ? this.state.totalAssets - amount 
                : this.state.totalAssets + amount;
            
            await set(summaryRef, {
                total: newTotal,
                last_updated: serverTimestamp()
            });

            this.currentEntryAmount = '0';
            document.getElementById('amount-display').textContent = '0';
            alert('登録完了しました');
            this.switchView('dashboard');
        } catch (e) {
            console.error(e);
            alert('エラーが発生しました');
        }
    },

    switchView(viewId) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        const target = document.getElementById(viewId);
        if (target) target.classList.add('active');
        
        // Update Nav UI
        document.querySelectorAll('.nav-link').forEach(l => {
            l.classList.toggle('active', l.getAttribute('data-view') === viewId);
        });

        this.state.currentView = viewId;

        // Auto-close sidebar on mobile/tablet after selection
        this.toggleSidebar(false);
    },

    toggleSidebar(force) {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (force === undefined) {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        } else if (force === false) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        } else {
            sidebar.classList.add('active');
            overlay.classList.add('active');
        }
    },

    updateClock() {
        const clock = document.getElementById('system-clock');
        if (clock) {
            const now = new Date();
            clock.textContent = now.toLocaleTimeString('ja-JP', { hour12: false });
        }
    },

    updateAllocationUI() {
        const savings = Math.floor(this.state.monthlySalary * (this.state.allocationRatio / 100));
        const consumption = this.state.monthlySalary - savings;
        
        document.getElementById('label-savings').textContent = `貯蓄・投資 (${this.state.allocationRatio}%)`;
        document.getElementById('label-consumption').textContent = `生活費・消費 (${100 - this.state.allocationRatio}%)`;
        document.getElementById('allocation-result').textContent = `¥${savings.toLocaleString()} / ¥${consumption.toLocaleString()}`;
    },

    updateDashboardStats() {
        document.getElementById('total-assets-val').textContent = `¥${this.state.totalAssets.toLocaleString()}`;
        this.updateAllocationUI();
    },

    renderHistory() {
        const containers = [
            document.getElementById('recent-list'), // Dashboard view (not in HTML yet but maybe in older versions)
            document.getElementById('history-container') // History view
        ];
        
        const html = this.state.history.slice(0, 50).map(item => `
            <div class="history-item">
                <div style="display: flex; align-items: center; gap: 1.2rem;">
                    <div class="history-icon ${item.type}"></div>
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">${item.category}</div>
                        <div style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-dim);">${item.date}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: var(--font-heading); font-weight: 700; font-size: 1.1rem; color: ${item.type === 'income' ? 'var(--primary)' : '#fff'};">
                        ${item.type === 'income' ? '+' : '-'}${item.amount.toLocaleString()}
                    </div>
                </div>
            </div>
        `).join('');

        containers.forEach(c => { if(c) c.innerHTML = html; });
    },

    charts: { asset: null, category: null },
    renderCharts() {
        // Global Chart.js Defaults
        Chart.defaults.font.family = "'Space Grotesk', sans-serif";
        Chart.defaults.color = '#888';

        // Asset Chart
        const assetCtx = document.getElementById('assetChart');
        if (assetCtx) {
            if (this.charts.asset) this.charts.asset.destroy();
            
            const labels = [];
            const data = [];
            this.state.history.slice(0, 10).reverse().forEach(h => {
                labels.push(h.date.split('-').slice(1).join('/'));
                data.push(h.amount);
            });

            this.charts.asset = new Chart(assetCtx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: labels.length ? labels : ['05/01', '05/02'],
                    datasets: [{
                        label: 'VALUATION',
                        data: data.length ? data : [1200000, 1250000],
                        borderColor: '#FF0000',
                        backgroundColor: 'rgba(255, 0, 0, 0.05)',
                        fill: true,
                        tension: 0.1,
                        borderWidth: 2,
                        pointBackgroundColor: '#FF0000',
                        pointBorderColor: '#fff',
                        pointRadius: 3,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(18, 20, 20, 0.95)',
                            titleFont: { size: 10, weight: 'bold' },
                            bodyFont: { size: 12 },
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        y: { 
                            grid: { color: 'rgba(255,255,255,0.03)' },
                            border: { display: false }
                        },
                        x: { 
                            grid: { display: false }
                        }
                    }
                }
            });
        }

        // Category Chart
        const categoryCtx = document.getElementById('categoryChart');
        if (categoryCtx) {
            if (this.charts.category) this.charts.category.destroy();
            
            const cats = {};
            this.state.history.forEach(h => {
                cats[h.category] = (cats[h.category] || 0) + h.amount;
            });
            
            const labels = Object.keys(cats).length ? Object.keys(cats) : ['食費', '固定費', '投資'];
            const data = Object.values(cats).length ? Object.values(cats) : [40, 35, 25];

            this.charts.category = new Chart(categoryCtx.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            'rgba(255, 255, 255, 0.1)',
                            'rgba(255, 0, 0, 0.8)',
                            'rgba(255, 255, 255, 0.4)',
                            'rgba(255, 255, 255, 0.05)',
                        ],
                        borderWidth: 1,
                        borderColor: 'rgba(0,0,0,0.5)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                boxWidth: 8,
                                font: { size: 10 }
                            }
                        }
                    }
                }
            });
        }

        // Analysis View Chart
        const analysisCtx = document.getElementById('categoryPieChart');
        if (analysisCtx) {
            if (this.charts.analysis) this.charts.analysis.destroy();
            this.charts.analysis = new Chart(analysisCtx.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['食費', '日用品', '娯楽', '交通', '住宅', 'その他'],
                    datasets: [{
                        label: 'EXPENSE_BY_CAT',
                        data: [12000, 19000, 3000, 5000, 2000, 3000],
                        backgroundColor: 'rgba(255, 0, 0, 0.6)',
                        borderColor: '#FF0000',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { grid: { color: 'rgba(255,255,255,0.05)' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    },

    currentEntryAmount: '0',
    keypadInput(val) {
        const display = document.getElementById('amount-display');
        if (val === 'C') {
            this.currentEntryAmount = '0';
        } else if (val === '00' && this.currentEntryAmount === '0') {
            return;
        } else {
            if (this.currentEntryAmount === '0') {
                this.currentEntryAmount = val;
            } else {
                this.currentEntryAmount += val;
            }
        }
        display.textContent = parseInt(this.currentEntryAmount).toLocaleString();
    }
};

// Expose to window for global access (like onclick handlers)
window.app = app;
window.onload = () => app.init();
