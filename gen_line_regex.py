import os
import re
import codecs

line_logs_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'
members_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members'

# 1. Get all unique speakers from line logs
speakers = set()
for filename in os.listdir(line_logs_dir):
    if filename.startswith('[整理済み]') and filename.endswith('.md'):
        path = os.path.join(line_logs_dir, filename)
        with codecs.open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'発言者:\n(.*?)\n整理情報:', content, re.DOTALL)
            if match:
                names = re.findall(r'- "(.*?)"', match.group(1))
                for n in names:
                    speakers.add(n)

# 2. Generate Table for LINE Name Regex Mapping
table_lines = [
    "# LINE名・正規表現設定シート",
    "",
    "このファイルは、LINEログに登場する「表示名」を正規表現で定義するためのシートです。",
    "C列に、そのLINE名を特定するための最終的な正規表現を記入してください。",
    "",
    "| A列: LINE表示名 | B列: 推測される正規表現 | C列: カスタム正規表現 (ユーザー入力) |",
    "| :--- | :--- | :--- |"
]

for s in sorted(list(speakers)):
    # Simple escaping for regex
    escaped_s = re.escape(s)
    # Most likely regex is just exact match
    guess = f"^{escaped_s}$"
    table_lines.append(f"| {s} | {guess} | |")

output_path = os.path.join(members_dir, 'line_name_regex.md')
with codecs.open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(table_lines))

print(f'Generated LINE name regex sheet for {len(speakers)} names at {output_path}')
