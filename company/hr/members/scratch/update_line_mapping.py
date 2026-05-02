import os
import yaml
import re
import csv

MEMBER_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
LOG_DIR = os.path.join(MEMBER_DIR, "line_logs")
OUTPUT_CSV = os.path.join(MEMBER_DIR, "_archive", "line_mapping_pending.csv")

def get_known_line_names():
    known = set(["大谷 彩人", "SaitoOtani"])
    for f in os.listdir(MEMBER_DIR):
        if not f.endswith(".md") or f.startswith("_"): continue
        path = os.path.join(MEMBER_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) >= 2:
                data = yaml.safe_load(parts[1])
                if data and "line_names" in data:
                    names = data["line_names"]
                    if isinstance(names, list):
                        known.update(names)
                    elif names:
                        known.add(str(names))
                if data and "name" in data:
                    known.add(data["name"])
        except:
            pass
    return known

def get_log_speakers():
    speakers = set()
    for f in os.listdir(LOG_DIR):
        if not f.endswith(".md"): continue
        path = os.path.join(LOG_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) >= 2:
                data = yaml.safe_load(parts[1])
                if data and "speakers" in data:
                    s_list = data["speakers"]
                    for s in s_list:
                        # [[Name]] 形式を解除
                        clean_name = s.replace("[[", "").replace("]]", "")
                        speakers.add(clean_name)
        except:
            pass
    return speakers

def update_pending_csv():
    known = get_known_line_names()
    speakers = get_log_speakers()
    
    unknown = speakers - known
    
    # 既存のCSVを読み込む
    existing_entries = []
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            existing_entries = list(reader)
            
    existing_line_names = set(row['line_name_in_log'] for row in existing_entries if row.get('line_name_in_log'))
    
    # 新しい不明な名前を追加
    new_rows = []
    for name in sorted(list(unknown)):
        if name not in existing_line_names and name not in ["大谷 彩人", "Owner"]:
            new_rows.append({
                "type": "Unknown (From Log)",
                "name": "",
                "line_name_in_log": name,
                "category": "",
                "filename": ""
            })
            
    # 書き出し
    fieldnames = ["type", "name", "line_name_in_log", "category", "filename"]
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_entries)
        writer.writerows(new_rows)
        
    print(f"Added {len(new_rows)} new unknown names to {OUTPUT_CSV}")

if __name__ == "__main__":
    update_pending_csv()
