import os
import re
import codecs

base_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'

# Patterns for extraction
date_header_pattern = re.compile(r'^## (\d{4}\.\d{2}\.\d{2} .+)$')
# Format from previous step: - **12:48 Name**: Message
msg_line_pattern = re.compile(r'^- \*\*(\d{2}:\d{2}) (.+?)\*\*: (.*)$')

files = [f for f in os.listdir(base_dir) if f.startswith('[整理済み]') and f.endswith('.txt')]

processed_count = 0

for filename in files:
    txt_path = os.path.join(base_dir, filename)
    md_filename = filename.replace('.txt', '.md')
    md_path = os.path.join(base_dir, md_filename)
    
    try:
        with codecs.open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue
    
    lines = content.split('\n')
    
    speakers = set()
    dates = []
    message_count = 0
    
    for line in lines:
        line = line.strip()
        date_match = date_header_pattern.match(line)
        if date_match:
            dates.append(date_match.group(1))
            continue
            
        msg_match = msg_line_pattern.match(line)
        if msg_match:
            time, name, msg = msg_match.groups()
            speakers.add(name.strip())
            message_count += 1

    # Manual YAML generation
    target_person = filename.replace('[整理済み]', '').replace('.txt', '').strip()
    
    yaml_lines = [
        "---",
        f"登場人物:",
        f"  - \"{target_person}\"",
        "発言者:"
    ]
    for s in sorted(list(speakers)):
        # Escape quotes in names if any
        s_esc = s.replace('"', '\\"')
        yaml_lines.append(f"  - \"{s_esc}\"")
        
    yaml_lines.extend([
        "整理情報:",
        f"  開始日: \"{dates[0] if dates else '不明'}\"",
        f"  終了日: \"{dates[-1] if dates else '不明'}\"",
        f"  メッセージ件数: {message_count}",
        "  状態: \"整理済み\"",
        "---",
        ""
    ])
    
    frontmatter = "\n".join(yaml_lines)
    md_content = frontmatter + content
    
    with codecs.open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Delete original txt
    os.remove(txt_path)
    processed_count += 1

print(f'Converted {processed_count} files to Markdown with properties.')
