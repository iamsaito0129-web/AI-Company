import os
import re
import codecs
import shutil

base_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'
archive_dir = os.path.join(base_dir, 'archive')

# 1. Get original files from archive
original_files = [f for f in os.listdir(archive_dir) if f.startswith('[済]') and f.endswith('.txt')]

date_pattern = re.compile(r'^\d{4}\.\d{2}\.\d{2} \S+$')
time_prefix_pattern = re.compile(r'^(\d{2}:\d{2})\s+(.*)$')

processed_count = 0

for filename in original_files:
    filepath = os.path.join(archive_dir, filename)
    # The basename for [整理済み] and [済] should be the same
    basename = filename[len('[済]'):]
    
    # Read content
    try:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with codecs.open(filepath, 'r', encoding='shift_jis') as f:
                lines = f.readlines()
        except Exception as e:
            print(f'Error reading {filename}: {e}')
            continue

    # --- Phase 1: Name Identification ---
    # Collect all lines that start with HH:MM
    msg_headers = []
    for line in lines:
        line = line.rstrip()
        m = time_prefix_pattern.match(line)
        if m:
            msg_headers.append(m.group(2)) # The "Name Message" part
            
    # Count frequency of space-separated prefixes
    prefix_counts = {}
    for header in msg_headers:
        parts = header.split(' ')
        # We assume a name can be up to 3 words long
        for i in range(1, min(len(parts), 4)):
            prefix = " ".join(parts[:i])
            prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
            
    # Determine the "best" names
    # Strategy: A prefix is a name if it's the longest prefix that appears consistently.
    # We'll build a set of identified names for this file.
    identified_names = set()
    sorted_prefixes = sorted(prefix_counts.keys(), key=lambda x: (len(x.split(' ')), len(x)), reverse=True)
    
    # For each header, pick the longest frequent prefix
    for header in msg_headers:
        for pref in sorted_prefixes:
            # It must be followed by a space or be the whole thing
            if header.startswith(pref + ' ') or header == pref:
                # If this prefix appears more than once, or it's the only one, we trust it
                if prefix_counts[pref] > 1 or len(sorted_prefixes) == 1:
                    identified_names.add(pref)
                    break
                elif prefix_counts[pref] == 1:
                    # If it only appears once, but it's long, maybe it's still a name
                    # But if a shorter version appears many times, prefer the shorter one?
                    # Actually, for LINE logs, names are usually consistent.
                    identified_names.add(pref)
                    break

    # --- Phase 2: Parsing ---
    parsed_lines = []
    current_date = ""
    message_count = 0
    unique_speakers = set()
    dates = []
    
    # Sort identified names by length descending for greedy matching
    sorted_id_names = sorted(list(identified_names), key=len, reverse=True)
    
    for line in lines:
        line = line.rstrip()
        if not line:
            parsed_lines.append("")
            continue
            
        if date_pattern.match(line):
            current_date = line
            dates.append(current_date)
            parsed_lines.append(f"\n## {line}\n")
            continue
            
        time_match = time_prefix_pattern.match(line)
        if time_match:
            time_str = time_match.group(1)
            rest = time_match.group(2)
            
            matched_name = None
            for name in sorted_id_names:
                if rest.startswith(name + ' ') or rest == name:
                    matched_name = name
                    break
            
            if matched_name:
                msg_body = rest[len(matched_name):].strip()
                parsed_lines.append(f"- **{time_str} {matched_name}**: {msg_body}")
                unique_speakers.add(matched_name)
                message_count += 1
            else:
                # Fallback: if no name identified, treat as continuation or system msg
                parsed_lines.append(f"  {line}")
        else:
            # Multi-line message continuation
            if parsed_lines:
                parsed_lines.append(f"  {line}")
            else:
                parsed_lines.append(line)

    # --- Phase 3: Output ---
    content = '\n'.join(parsed_lines)
    if message_count < 3 or len(content.strip()) < 100:
        content = "※このLINEログは内容がほとんどありません。\n\n" + content
        
    # Generate Properties
    target_person = basename.replace('.txt', '').strip()
    yaml_lines = [
        "---",
        f"登場人物:",
        f"  - \"{target_person}\"",
        "発言者:"
    ]
    for s in sorted(list(unique_speakers)):
        s_esc = s.replace('"', '\\"')
        yaml_lines.append(f"  - \"{s_esc}\"")
        
    yaml_lines.extend([
        "整理情報:",
        f"  開始日: \"{dates[0] if dates else '不明'}\"",
        f"  終了日: \"{dates[-1] if dates else '不明'}\"",
        f"  メッセージ件数: {message_count}",
        "  状態: \"整理済み (高精度解析)\"",
        "---",
        ""
    ])
    
    md_content = "\n".join(yaml_lines) + content
    md_path = os.path.join(base_dir, f'[整理済み]{basename.replace(".txt", ".md")}')
    
    with codecs.open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    processed_count += 1

print(f'Re-processed {processed_count} files with improved name detection.')
