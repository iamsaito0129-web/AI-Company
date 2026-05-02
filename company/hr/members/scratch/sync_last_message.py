import os
import yaml
import re
from datetime import datetime

MEMBER_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
LOG_DIR = os.path.join(MEMBER_DIR, "line_logs")

def get_latest_dates_from_logs():
    speaker_latest = {} # speaker_name -> date_string
    
    if not os.path.exists(LOG_DIR):
        return speaker_latest
        
    for f in os.listdir(LOG_DIR):
        if not f.endswith(".md"): continue
        path = os.path.join(LOG_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # YAMLフロントマターから speakers と date_range (エンド) を取得
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 2: continue
            data = yaml.safe_load(parts[1])
            if not data or "speakers" not in data: continue
            
            # 日付の特定
            # 優先1: 本文内の見出し ## YYYY.MM.DD
            # 優先2: フロントマターの date_range
            
            # まず本文から日付とスピーカーの出現を紐付け
            dates_in_file = re.findall(r'^## (\d{4})\.(\d{2})\.(\d{2})', content, re.MULTILINE)
            current_date = None
            if len(parts) > 2:
                body = parts[2]
                lines = body.split('\n')
                for line in lines:
                    date_match = re.match(r'^## (\d{4})\.(\d{2})\.(\d{2})', line)
                    if date_match:
                        current_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                    
                    if current_date:
                        # スピーカーの出現を探す [[名前]]
                        found_speakers = re.findall(r'\[\[([^\]]+)\]\]', line)
                        for s in found_speakers:
                            s = s.strip()
                            if s not in speaker_latest or current_date > speaker_latest[s]:
                                speaker_latest[s] = current_date
            
            # 本文から取れなかった場合のバックアップ (date_range)
            if not dates_in_file and "date_range" in data:
                dr = data["date_range"]
                # "2025-04-24 to 2025-04-25" または "2025-04-24"
                dates = re.findall(r'\d{4}-\d{2}-\d{2}', str(dr))
                if dates:
                    latest_dr = max(dates)
                    for s in data["speakers"]:
                        s = s.replace("[[", "").replace("]]", "").strip()
                        if s not in speaker_latest or latest_dr > speaker_latest[s]:
                            speaker_latest[s] = latest_dr
                            
        except Exception as e:
            print(f"Error processing log {f}: {e}")
            
    return speaker_latest

def update_members(speaker_latest):
    updated_count = 0
    for f in os.listdir(MEMBER_DIR):
        if not f.endswith(".md") or f.startswith("_"): continue
        path = os.path.join(MEMBER_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 2: continue
            data = yaml.safe_load(parts[1])
            if not data: continue
            
            name = data.get("name", os.path.splitext(f)[0])
            line_names = data.get("line_names", [])
            if line_names is None: line_names = []
            if isinstance(line_names, str): line_names = [line_names]
            
            all_possible_names = [name] + line_names
            
            latest_date = None
            for n in all_possible_names:
                if n in speaker_latest:
                    if not latest_date or speaker_latest[n] > latest_date:
                        latest_date = speaker_latest[n]
            
            if latest_date:
                # プロパティを更新
                data["last_contact_line"] = latest_date
                
                new_frontmatter = yaml.dump(data, allow_unicode=True, sort_keys=False).strip()
                new_content = f"---\n{new_frontmatter}\n---" + (parts[2] if len(parts) > 2 else "")
                
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                updated_count += 1
                
        except Exception as e:
            print(f"Error updating member {f}: {e}")
            
    print(f"Successfully synced last contact dates for {updated_count} members.")

if __name__ == "__main__":
    print("Extracting latest dates from logs...")
    speaker_dates = get_latest_dates_from_logs()
    print(f"Found latest dates for {len(speaker_dates)} speakers.")
    print("Updating member files...")
    update_members(speaker_dates)
