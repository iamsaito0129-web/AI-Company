import json
import os

data_path = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\finance\data\master\dashboard_view.json'
html_path = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\finance\specs\dashboard_final.html'

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

top_expenses = data.get('top_expenses', [])

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# カテゴリUIの構築
category_html = """
                    <div class="mb-8">
                        <h3 class="font-mono text-lg font-bold text-white mb-6 flex items-center gap-2 uppercase tracking-tighter">
                            <span class="material-symbols-outlined text-accent">pie_chart</span>
                            Expense_Categories
                        </h3>
                        <div class="flex flex-wrap gap-3">
"""
for cat, amt in top_expenses:
    category_html += f"""
                            <div class="glass-card px-4 py-2 rounded-xl border border-white/5">
                                <p class="text-[10px] text-slate-400 uppercase font-mono">{cat}</p>
                                <p class="font-bold text-sm">¥ {amt:,}</p>
                            </div>
"""
category_html += """
                        </div>
                    </div>
"""

# HTMLの置換
target = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="asset-list">'
new_html = html.replace(target, category_html + target)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("UI Updated successfully")
