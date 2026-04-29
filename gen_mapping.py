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
            # Try to extract speakers from frontmatter
            match = re.search(r'発言者:\n(.*?)\n整理情報:', content, re.DOTALL)
            if match:
                names = re.findall(r'- "(.*?)"', match.group(1))
                for n in names:
                    speakers.add(n)

# 2. Get all member names
member_files = [f.replace('.md', '') for f in os.listdir(members_dir) if f.endswith('.md') and not f.startswith('_') and not f.startswith('member_input_sheet')]

# 3. Create mapping
mapping = []
for s in sorted(list(speakers)):
    guess = ""
    # Simple matching logic
    for m in member_files:
        if s in m or m in s:
            # Create a regex like ^Name.*$ or similar
            # If s is "三宅" and m is "三宅莉瑠", regex could be "^三宅.*$"
            if s == m:
                guess = f"^{s}$"
            else:
                guess = f"^{s}.*$"
            break
    mapping.append((s, guess))

# 4. Generate Markdown table
table_lines = [
    "# 名前・正規表現対応表",
    "",
    "| A列: 抽出された名前 | B列: 推測される正規表現 | C列: カスタム正規表現 |",
    "| :--- | :--- | :--- |"
]

for s, guess in mapping:
    table_lines.append(f"| {s} | {guess} | |")

output_path = os.path.join(members_dir, 'name_regex_mapping.md')
with codecs.open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(table_lines))

print(f'Generated mapping for {len(mapping)} names at {output_path}')
