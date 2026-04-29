import re
import json

def parse_member_mapping():
    file_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\name_regex_mapping.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    member_to_regex = {}
    for line in lines:
        if not line.startswith('|') or ":---" in line or "A列" in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            member_name = parts[1]
            regex_raw = parts[3] # C列
            if regex_raw:
                # パイプで分割。括弧や先頭の(などは除去
                clean_regex = regex_raw.strip('()')
                patterns = [p.strip() for p in clean_regex.split('|') if p.strip()]
                member_to_regex[member_name] = patterns
            else:
                member_to_regex[member_name] = []
    
    return member_to_regex

def get_line_mapping():
    # 前回の分析結果を再利用
    file_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    display_names = []
    for i in range(7, len(lines)):
        line = lines[i].strip()
        if not line.startswith('|'): break
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            name = parts[1]
            if name and name != "A列: LINE表示名" and name != ":---":
                display_names.append(name)
    
    regex_list = []
    start_collecting = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if line == "C列": start_collecting = True; continue
        if start_collecting and line: regex_list.append(line)

    mapping = {}
    limit = min(len(display_names), len(regex_list))
    for i in range(limit):
        mapping[display_names[i]] = regex_list[i]
    return mapping

def finalize():
    member_to_regex = parse_member_mapping()
    line_display_to_regex = get_line_mapping()

    # 表示名 -> メンバー名 への直接変換辞書
    display_to_member = {}
    
    for display_name, regex in line_display_to_regex.items():
        found = False
        for member, patterns in member_to_regex.items():
            if regex in patterns:
                display_to_member[display_name] = member
                found = True
                break
        if not found:
            # 正規表現がメンバー表にない場合、正規表現の見た目から推測（^名前$ 形式ならその名前）
            m = re.match(r'^\^(.+)\$$', regex)
            if m:
                display_to_member[display_name] = m.group(1)
            else:
                display_to_member[display_name] = display_name # フォールバック

    print(f"Created conversion map for {len(display_to_member)} display names.")
    
    with open("final_conversion_map.json", "w", encoding="utf-8") as f:
        json.dump(display_to_member, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    finalize()
