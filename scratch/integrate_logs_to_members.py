import os
import glob
import re
import json

# 設定
logs_dir = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
members_dir = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
mapping_file = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"

def get_mapping():
    mapping = {} # 正規表現 -> 正規名
    if not os.path.exists(mapping_file):
        return mapping
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    regex = parts[2]
                    canon = parts[3]
                    if regex and canon and canon != "名前が不足" and canon != "正規表現":
                        mapping[regex] = canon
    return mapping

def get_member_files():
    # 名前 -> ファイルパス
    members = {}
    files = glob.glob(os.path.join(members_dir, "*.md"))
    for f in files:
        if os.path.basename(f).startswith("_") or os.path.basename(f) == "line_name_regex.md" or os.path.basename(f) == "name_regex_mapping.md" or os.path.basename(f) == "member_input_sheet.md":
            continue
        name = os.path.splitext(os.path.basename(f))[0]
        members[name] = f
    return members

def update_members_with_logs():
    mapping = get_mapping()
    member_files = get_member_files()
    
    # 正規名 -> ログファイルのリスト
    name_to_logs = {}
    log_files = glob.glob(os.path.join(logs_dir, "*.md"))
    
    for log_path in log_files:
        log_name = os.path.basename(log_path)
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # YAMLフロントマッターからspeakersを抽出
            yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if yaml_match:
                yaml_text = yaml_match.group(1)
                speakers = re.findall(r'^\s*-\s+(.*)$', yaml_text, re.MULTILINE)
                for s in speakers:
                    s = s.strip().strip('"').strip("'")
                    # [[Name]] 形式からブラケットを除去
                    s_clean = s.strip("[").strip("]")
                    # 正規表現そのものが書かれている場合があるため、マッピングを通す
                    resolved_name = s_clean
                    for regex, canon in mapping.items():
                        if s_clean == regex:
                            resolved_name = canon
                            break
                    
                    if resolved_name not in name_to_logs:
                        name_to_logs[resolved_name] = set()
                    name_to_logs[resolved_name].add(log_name)

    # 各メンバーファイルを更新
    for name, filepath in member_files.items():
        if name in name_to_logs:
            logs = sorted(list(name_to_logs[name]))
            links = []
            for l in logs:
                basename = os.path.splitext(l)[0]
                # [[ ]] の内側に [ ] があるとObsidianでリンクが壊れる場合があるため
                # [ ] を含む場合はエイリアス形式 [[file|alias]] を使用
                if "[" in basename:
                    links.append(f"- [[{basename}|{basename}]]")
                else:
                    links.append(f"- [[{basename}]]")
            log_links = "\n".join(links)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            section_header = "## 📂 関連LINEログ"
            new_section = f"{section_header}\n{log_links}\n"
            
            if section_header in content:
                # 既存セクションを置換
                content = re.sub(f"{section_header}.*?(?=\n##|\Z)", new_section, content, flags=re.DOTALL)
            else:
                # 最後に追加
                content += f"\n{new_section}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {name}")

if __name__ == "__main__":
    update_members_with_logs()
    print("Integration complete.")
