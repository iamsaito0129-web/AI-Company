import os
import re
import requests
import json
import sys
from datetime import datetime

# Force UTF-8 for output to avoid cp932 errors on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- Configuration ---
FIREBASE_URL = "https://oku-jissenn-default-rtdb.firebaseio.com"
USER_ID = "saito"
DASHBOARD_PATH = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\lifestyle\finance\asset_dashboard.md"
LEDGER_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\lifestyle\ledgers"

def extract_total_assets(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Find "| **総資産** | **¥377,600** |"
            match = re.search(r"\|\s+\*\*総資産\*\*\s+\|\s+\*\*(?:¥|\\)([\d,]+)\*\*", content)
            
            if match:
                amount_str = match.group(1).replace(",", "")
                return int(amount_str)
    except Exception as e:
        print(f"Error reading dashboard: {e}")
    return None

def parse_ledger(file_path):
    records = []
    if not os.path.exists(file_path):
        return records
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        in_log = False
        for line in lines:
            if "## 支出明細 (Log)" in line:
                in_log = True
                continue
            if in_log and line.strip().startswith("- [x]"):
                # - [x] 2026-03-01 | 家賃 | \75,000 | 固定費 | 振込 |
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    date_part = parts[0].replace("- [x]", "").strip()
                    item = parts[1]
                    # Handle \ or ¥ or just numbers
                    amount_str = parts[2].replace("\\", "").replace("¥", "").replace(",", "").strip()
                    try:
                        amount = int(amount_str)
                        category = parts[3]
                        records.append({
                            "date": date_part,
                            "item": item,
                            "amount": amount,
                            "category": category,
                            "type": "expense"
                        })
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error parsing ledger {file_path}: {e}")
    return records

def upload_to_rtdb(total_assets, history_records):
    # 1. Update Assets Summary
    summary_path = f"{FIREBASE_URL}/users/{USER_ID}/assets/summary.json"
    summary_data = {
        "total": total_assets,
        "updatedAt": {".sv": "timestamp"}
    }
    
    print(f"Updating summary at {summary_path}...")
    try:
        response = requests.patch(summary_path, json=summary_data)
        if response.status_code == 200:
            print("[SUCCESS] Summary updated.")
        else:
            print(f"[ERROR] Failed to update summary: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] Summary update failed: {e}")

    # 2. Update History Records
    grouped = {}
    for r in history_records:
        try:
            date_obj = datetime.strptime(r["date"], "%Y-%m-%d")
            year = str(date_obj.year)
            month = f"{date_obj.month:02d}"
            if year not in grouped: grouped[year] = {}
            if month not in grouped[year]: grouped[year][month] = []
            grouped[year][month].append(r)
        except Exception as e:
            print(f"Skipping record with bad date: {r.get('date')} - {e}")

    for year, months in grouped.items():
        for month, records in months.items():
            history_path = f"{FIREBASE_URL}/history/{USER_ID}/{year}/{month}/records.json"
            print(f"Updating history for {year}-{month} at {history_path}...")
            
            record_dict = {f"rec_{i}": r for i, r in enumerate(records)}
            
            try:
                response = requests.put(history_path, json=record_dict)
                if response.status_code == 200:
                    print(f"[SUCCESS] History for {year}-{month} updated.")
                else:
                    print(f"[ERROR] Failed to update history: {response.status_code}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"[EXCEPTION] History update failed: {e}")

if __name__ == "__main__":
    print("Starting Sync...")
    total = extract_total_assets(DASHBOARD_PATH)
    
    all_history = []
    if os.path.exists(LEDGER_DIR):
        for filename in os.listdir(LEDGER_DIR):
            if re.match(r"\d{4}-\d{2}\.md", filename):
                ledger_path = os.path.join(LEDGER_DIR, filename)
                print(f"Parsing ledger: {filename}...")
                all_history.extend(parse_ledger(ledger_path))

    if total is not None:
        print(f"Total Assets: JPY {total:,}")
        upload_to_rtdb(total, all_history)
    else:
        print("[ERROR] Could not find Total Assets in dashboard file.")
