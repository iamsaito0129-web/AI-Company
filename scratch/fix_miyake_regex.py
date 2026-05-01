import os
import sys

path = r'C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md'

if not os.path.exists(path):
    print(f"File not found: {path}")
    sys.exit(1)

with open(path, 'rb') as f:
    content = f.read().decode('utf-8')

lines = content.splitlines()
new_lines = []
found = False

for l in lines:
    if '実委 みやけ  りる' in l:
        parts = l.split('|')
        if len(parts) >= 4:
            parts[3] = ' 三宅莉瑠 '
            new_l = '|'.join(parts)
            new_lines.append(new_l)
            found = True
        else:
            new_lines.append(l)
    else:
        new_lines.append(l)

if found:
    with open(path, 'wb') as f:
        f.write('\n'.join(new_lines).encode('utf-8'))
    print("UPDATED: '実委 みやけ  りる' -> '三宅莉瑠'")
else:
    print("NOT FOUND: '実委 みやけ  りる'")
