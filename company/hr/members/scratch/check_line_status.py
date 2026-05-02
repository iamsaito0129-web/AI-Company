import os
import yaml
import re
import csv
import sys

# Windowsでの文字化け対策
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MEMBER_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
LOG_DIR = os.path.join(MEMBER_DIR, "line_logs")
INPUT_CSV = os.path.join(MEMBER_DIR, "line_names_input_sheet.csv")

def get_members_info():
    members = {}
    for f in os.listdir(MEMBER_DIR):
        if f.endswith(".md") and not f.startswith("_"):
            path = os.path.join(MEMBER_DIR, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
                if len(parts) >= 2:
                    data = yaml.safe_load(parts[1])
                    if data:
                        name = data.get("name")
                        if not name:
                            name = os.path.splitext(f)[0]
                        line_names = data.get("line_names", [])
                        if line_names is None: line_names = []
                        if isinstance(line_names, str): line_names = [line_names]
                        members[name] = {
                            "filename": f,
                            "line_names": [ln for ln in line_names if ln],
                            "category": data.get("category", "")
                        }
            except Exception:
                pass
    return members

def get_log_speakers():
    speakers = set()
    if not os.path.exists(LOG_DIR):
        return speakers
    for f in os.listdir(LOG_DIR):
        if f.endswith(".md"):
            path = os.path.join(LOG_DIR, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
                if len(parts) >= 2:
                    data = yaml.safe_load(parts[1])
                    if data and "speakers" in data:
                        for s in data["speakers"]:
                            s = s.replace("[[", "").replace("]]", "").strip()
                            if s:
                                speakers.add(s)
            except Exception:
                pass
    return speakers

def main():
    members = get_members_info()
    log_speakers = get_log_speakers()
    
    # 1. LINE名が未入力のメンバー
    empty_line_names = sorted([name for name, info in members.items() if not info["line_names"]])
    print(f"### LINE名が未入力のメンバー ({len(empty_line_names)}名):")
    for name in empty_line_names:
        print(f"- {name}")
    
    # 2. ログには登場するが、誰のものか特定されていないLINE名
    all_registered_line_names = set()
    for name, info in members.items():
        all_registered_line_names.add(name)
        for ln in info["line_names"]:
            all_registered_line_names.add(ln)
            
    csv_line_names = set()
    if os.path.exists(INPUT_CSV):
        with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("line_names"):
                    csv_line_names.add(row["line_names"])
                    
    unknown_speakers = []
    for s in log_speakers:
        if s not in all_registered_line_names and s not in csv_line_names:
            unknown_speakers.append(s)
            
    print(f"\n### ログに登場するが未紐付けのLINE名 ({len(unknown_speakers)}件):")
    if not unknown_speakers:
        print("- なし")
    else:
        for s in sorted(unknown_speakers):
            print(f"- {s}")

if __name__ == "__main__":
    main()
