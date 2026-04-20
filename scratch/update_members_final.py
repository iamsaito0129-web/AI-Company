import os
import re

members_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members'
sheet_path = os.path.join(members_dir, 'member_input_sheet.md')

def update_member_files():
    if not os.path.exists(sheet_path):
        print("Sheet not found.")
        return

    with open(sheet_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse table
    data = []
    for line in lines:
        if '|' in line and not line.startswith('| :---') and not line.startswith('#') and '元のファイル名' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                file_name = parts[1]
                kanji_name = parts[2]
                kana_name = parts[3]
                data.append((file_name, kanji_name, kana_name))

    for file_base, kanji, kana in data:
        file_path = os.path.join(members_dir, f'{file_base}.md')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update properties
            # Ensure kanji_name and kana_name exist
            if 'kanji_name:' not in content:
                content = re.sub(r'name: "(.*?)"', rf'name: "\1"\nkanji_name: "{kanji}"\nkana_name: "{kana}"', content)
            else:
                content = re.sub(r'kanji_name: "(.*?)"', f'kanji_name: "{kanji}"', content)
                content = re.sub(r'kana_name: "(.*?)"', f'kana_name: "{kana}"', content)

            # Update last_updated
            content = re.sub(r'last_updated: "(.*?)"', 'last_updated: "2026-04-20"', content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_base}.md")
        else:
            print(f"File {file_base}.md not found.")

if __name__ == "__main__":
    update_member_files()
