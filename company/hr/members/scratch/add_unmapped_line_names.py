import os
import yaml
import csv
import re

# パス設定
BASE_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
MEMBER_DIR = BASE_DIR
INPUT_CSV = os.path.join(BASE_DIR, "line_names_input_sheet.csv")
REGEX_MD = os.path.join(BASE_DIR, "line_name_regex.md")

def get_mapped_line_names():
    mapped_names = set()
    for filename in os.listdir(MEMBER_DIR):
        if filename.endswith(".md") and not filename.startswith("_"):
            filepath = os.path.join(MEMBER_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) >= 2:
                try:
                    data = yaml.safe_load(parts[1])
                    if data and "line_names" in data:
                        lns = data["line_names"]
                        if isinstance(lns, list):
                            for n in lns:
                                if n: mapped_names.add(n)
                        elif isinstance(lns, str) and lns:
                            mapped_names.add(lns)
                except:
                    pass
    return mapped_names

def get_all_line_display_names():
    display_names = set()
    if not os.path.exists(REGEX_MD):
        return display_names
        
    with open(REGEX_MD, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(8, len(lines)):
        line = lines[i].strip()
        if not line.startswith('|'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            name = parts[1]
            if name and name not in ["A列: LINE表示名", ":---", "---"]:
                display_names.add(name)
    return display_names

def update_input_sheet():
    mapped = get_mapped_line_names()
    all_line = get_all_line_display_names()
    
    # 紐付けられていないLINE名
    unmapped = sorted(list(all_line - mapped))
    
    # 既存のCSVを読み込む
    existing_rows = []
    if os.path.exists(INPUT_CSV):
        with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            existing_rows = list(reader)
            
    # 未紐付けLINE名を追加
    # すでにCSVにあるかチェック
    existing_line_names_in_csv = set()
    for row in existing_rows:
        if row.get("line_names"):
            existing_line_names_in_csv.add(row["line_names"])
            
    new_rows = []
    for ln in unmapped:
        if ln not in existing_line_names_in_csv:
            new_rows.append({
                "name": "未紐付け",
                "line_names": ln,
                "category": "LINEログに存在",
                "filename": ""
            })
            
    # 書き出し
    fieldnames = ["name", "line_names", "category", "filename"]
    with open(INPUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)
        writer.writerows(new_rows)
        
    print(f"Added {len(new_rows)} unmapped line names to {INPUT_CSV}")

if __name__ == "__main__":
    update_input_sheet()
