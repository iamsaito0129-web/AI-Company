import os
import re
import glob
import codecs
import shutil

base_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'
archive_dir = os.path.join(base_dir, 'archive')

if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

files = []
for root, dirs, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.startswith('[LINE]') and filename.endswith('.txt'):
            files.append(os.path.join(root, filename))

date_pattern = re.compile(r'^\d{4}\.\d{2}\.\d{2} \S+$')
msg_pattern = re.compile(r'^(\d{2}:\d{2})\t([^\t]+)\t(.*)$')
msg_pattern_alt = re.compile(r'^(\d{2}:\d{2})\s+(.+?)\s+(.*)$') # fallback if spaces instead of tabs

processed_count = 0

for filepath in files:
    filename = os.path.basename(filepath)
    basename = filename[len('[LINE]'):]
    new_filename = f'[整理済み]{basename}'
    new_filepath = os.path.join(base_dir, new_filename)
    
    # Process content
    try:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with codecs.open(filepath, 'r', encoding='shift_jis') as f:
                lines = f.readlines()
        except Exception as e:
            print(f'Error reading {filepath}: {e}')
            continue

    parsed_lines = []
    message_count = 0
    
    for line in lines:
        line = line.rstrip()
        if not line:
            parsed_lines.append("")
            continue
            
        if date_pattern.match(line):
            parsed_lines.append(f"\n## {line}\n")
        else:
            m = msg_pattern.match(line)
            if not m:
                m = msg_pattern_alt.match(line)
            if m:
                time, name, msg = m.groups()
                parsed_lines.append(f"- **{time} {name}**: {msg}")
                message_count += 1
            else:
                if "トーク履歴" in line or "保存日時" in line:
                    parsed_lines.append(f"# {line}")
                else:
                    parsed_lines.append(f"  {line}")
                    if line.strip() and not line.startswith("☎"): 
                        message_count += 1

    content = '\n'.join(parsed_lines)
    
    if message_count < 3 or len(content.strip()) < 100:
        header_note = "※このLINEログは内容がほとんどありません。\n\n"
        content = header_note + content
        
    # Write [整理済み] file
    with codecs.open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Move and rename original file
    done_filename = f'[済]{basename}'
    done_filepath = os.path.join(archive_dir, done_filename)
    
    try:
        if filepath != done_filepath:
            shutil.move(filepath, done_filepath)
        processed_count += 1
    except Exception as e:
        print(f'Error moving {filepath}: {e}')

print(f'Processed {processed_count} files.')
