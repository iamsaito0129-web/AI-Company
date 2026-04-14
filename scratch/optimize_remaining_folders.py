import os
import re

directories = [
    r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\secretary\knowledge",
    r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\projects",
    r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\engineering\docs"
]

def optimize_file(path):
    if not path.endswith('.md') or os.path.basename(path).startswith('_'):
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'obsidian-skills: optimized' in content:
        return

    filename = os.path.basename(path)
    title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ').title()
    
    # Simple tag extraction based on path
    tag = "knowledge"
    if 'projects' in path: tag = "project"
    elif 'engineering' in path: tag = "engineering"

    frontmatter = f"""---
title: "{title}"
date: {os.path.getmtime(path)}
tags:
  - {tag}
status: active
obsidian-skills: optimized
---

"""
    # Wikilink conversion for common references (rudimentary)
    new_body = re.sub(r'\[(.*?)\]\((.*?)\.md\)', r'[[\2|\1]]', content)
    
    # Add Callouts for sections
    new_body = re.sub(r'(# (?:Overview|概要|Summary))([\s\S]*?)(?=#|\Z)', r'> [!ABSTRACT]\1\2', new_body)
    new_body = re.sub(r'(## (?:Requirements|要件|TODO))([\s\S]*?)(?=#|\Z)', r'> [!TODO]\1\2', new_body)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + new_body)
    print(f"Optimized: {path}")

if __name__ == "__main__":
    for root_dir in directories:
        for root, dirs, files in os.walk(root_dir):
            if 'node_modules' in root: continue
            for file in files:
                optimize_file(os.path.join(root, file))
