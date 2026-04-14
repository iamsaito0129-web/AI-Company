import os
import re
from datetime import datetime

directory = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\ceo\decisions"

def optimize_decision(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already optimized in this session (simplified check)
    if 'obsidian-skills: optimized' in content:
        print(f"Already optimized: {os.path.basename(path)}")
        return

    # Basic metadata extraction
    filename = os.path.basename(path)
    title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', filename) or re.search(r'\d{8}', filename)
    date_str = date_match.group(0) if date_match else datetime.now().strftime('%Y-%m-%d')
    # Format date if 20260323
    if len(date_str) == 8 and date_str.isdigit():
        date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    # Properties
    frontmatter = f"""---
title: "{title}"
date: {date_str}
tags:
  - decision
  - ceo
status: resolved
obsidian-skills: optimized
---

"""
    
    # Body enhancement (Callouts)
    # If the file has a structure like "Decision: ..." or "Conclusion: ...", wrap in callout
    new_body = content
    if '### 決定事項' in content or '### Decision' in content or '## 決定' in content:
        # Simple wrap for demonstration (premium aesthetics)
        new_body = re.sub(r'(### (?:決定事項|Decision))([\s\S]*?)(?=###|\Z)', r'> [!IMPORTANT]\1\2', new_body)
    
    if '### 理由' in content or '### Reason' in content or '## 理由' in content:
        new_body = re.sub(r'(### (?:理由|Reason))([\s\S]*?)(?=###|\Z)', r'> [!NOTE]\1\2', new_body)

    final_content = frontmatter + new_body
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Optimized: {filename}")

if __name__ == "__main__":
    for file in os.listdir(directory):
        if file.endswith('.md') and file != '_template.md':
            optimize_decision(os.path.join(directory, file))
