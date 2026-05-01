import csv
import os

csv_path = r'C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\unknown_line_names.csv'
mapping_path = r'C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md'

if not os.path.exists(csv_path):
    print("CSV not found")
    exit(1)

new_rows = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        if not row: continue
        raw_name = row[0]
        canon_name = row[1] if len(row) > 1 else ""
        if not canon_name: canon_name = "名前が不足"
        
        # B列用の簡易的なエスケープ
        escaped = raw_name.replace(" ", "\\ ").replace("(", "\\(").replace(")", "\\)")
        row_str = f"| {raw_name} | ^{escaped}$ | {canon_name} |"
        new_rows.append(row_str)

if new_rows:
    with open(mapping_path, 'a', encoding='utf-8') as f:
        f.write("\n" + "\n".join(new_rows) + "\n")
    print(f"Added {len(new_rows)} rows to {mapping_path}")
else:
    print("No rows to add")
