import re
import json

def analyze_mapping():
    file_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # A列の抽出 (8行目から、テーブル形式が終わるまで)
    display_names = []
    for i in range(7, len(lines)):
        line = lines[i].strip()
        if not line.startswith('|'):
            break
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            name = parts[1]
            if name and name != "A列: LINE表示名" and name != ":---":
                display_names.append(name)
    
    print(f"Found {len(display_names)} display names in A column.")

    # C列の抽出 (986行目付近の 'C列' という見出し以降)
    regex_list = []
    start_collecting = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if line == "C列":
            start_collecting = True
            continue
        if start_collecting:
            if line:
                regex_list.append(line)
            else:
                # 空行があれば終了（または継続、状況によるが一旦空行は無視）
                continue
    
    print(f"Found {len(regex_list)} regex patterns in C column area.")

    # 紐付け
    mapping = {}
    limit = min(len(display_names), len(regex_list))
    for i in range(limit):
        mapping[display_names[i]] = regex_list[i]
    
    # 残りのチェック
    if len(display_names) != len(regex_list):
        print(f"Warning: Count mismatch! Names: {len(display_names)}, Regex: {len(regex_list)}")
    
    with open("mapping_debug.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print("Mapping saved to mapping_debug.json")

if __name__ == "__main__":
    analyze_mapping()
