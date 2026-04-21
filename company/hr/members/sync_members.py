import os
import re

# パス設定
MEMBERS_DIR = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members'
SHEET_PATH = os.path.join(MEMBERS_DIR, 'member_input_sheet.md')

def parse_sheet(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data = []
    table_started = False
    for line in lines:
        if '|' in line and '-' * 3 in line:
            table_started = True
            continue
        if table_started and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                # | index 0 | index 1 (old) | index 2 (new) | index 3 (kana) | index 4 (notes) |
                old_file = parts[1]
                new_kanji = parts[2]
                new_kana = parts[3]
                if old_file and new_kanji:
                    data.append({
                        'old': old_file,
                        'kanji': new_kanji,
                        'kana': new_kana
                    })
    return data

def update_member_file(item):
    old_path = os.path.join(MEMBERS_DIR, f"{item['old']}.md")
    new_path = os.path.join(MEMBERS_DIR, f"{item['kanji']}.md")
    
    # ファイルが見つからない場合の修正（リネーム済みの可能性）
    if not os.path.exists(old_path):
        if os.path.exists(new_path):
            target_path = new_path
        else:
            print(f"警告: {item['old']}.md が見つかりません。スキップします。")
            return
    else:
        target_path = old_path

    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatterの更新
    content = re.sub(r'kanji_name: ".*?"', f'kanji_name: "{item["kanji"]}"', content)
    content = re.sub(r'kana_name: ".*?"', f'kana_name: "{item["kana"]}"', content)
    content = re.sub(r'name: ".*?"', f'name: "{item["kanji"]}"', content)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # リネーム
    if item['old'] != item['kanji'] and os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"リネーム完了: {item['old']} -> {item['kanji']}")
    else:
        print(f"更新完了: {item['kanji']}")

def main():
    items = parse_sheet(SHEET_PATH)
    for item in items:
        update_member_file(item)

if __name__ == "__main__":
    main()
