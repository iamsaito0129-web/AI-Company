import os
import json
import re

members_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
entity_map_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"

def execute_merge_simple():
    with open(entity_map_path, 'r', encoding='utf-8') as f:
        entity_map = json.load(f)

    merges = [
        ("小松樹.md", ["いつき", "学校教育 いつき"]),
        ("山本哲大.md", ["やまもと"]),
        ("萩平智之.md", ["HAGI"]),
        ("吉崎アキラ.md", ["ざき"]),
        ("中山佳名子.md", ["中山"]),
    ]

    for formal_file, aliases in merges:
        path = os.path.join(members_dir, formal_file)
        if not os.path.exists(path):
            print(f"File not found: {formal_file}")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle aliases in frontmatter via regex
        # Check if aliases exists
        alias_pattern = re.compile(r'^aliases:\s*\[(.*?)\]', re.MULTILINE)
        if alias_pattern.search(content):
            def repl(m):
                existing = [x.strip().strip('"').strip("'") for x in m.group(1).split(',')]
                for a in aliases:
                    if a not in existing: existing.append(a)
                return f"aliases: [{', '.join(['\"' + x + '\"' for x in existing if x])}]"
            content = alias_pattern.sub(repl, content)
        else:
            # Add before tags or after name
            content = re.sub(r'(name: ".*?")', r'\1\naliases: [' + ', '.join(['"' + x + '"' for x in aliases]) + ']', content)

        # Update knowledge section
        all_chats = set()
        total_interactions = 0
        
        # Get formal name from file
        name_match = re.search(r'name: "(.*?)"', content)
        formal_name = name_match.group(1) if name_match else formal_file.replace('.md', '')
        
        for name in [formal_name] + aliases:
            if name in entity_map:
                all_chats.update(entity_map[name]['chats'])
                total_interactions += entity_map[name]['interactions']

        depth_section = f"\n## 📜 LINEログからの知見 (Relation Analysis)\n> [!TIP] 関係性の推定\n> - **主要な呼び名**: {', '.join(aliases)}\n> - **確認済み交流**: {total_interactions}件のログメッセージ\n> - **主要チャット**: {', '.join(list(all_chats)[:5])}など\n"
        
        if '## 📜 LINEログからの知見' in content:
            content = re.sub(r'## 📜 LINEログからの知見 \(Relation Analysis\).*?(\n##|$)', depth_section + r'\1', content, flags=re.DOTALL)
        else:
            content = content.replace('## 📝 ログ', depth_section + '\n## 📝 ログ')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Merged aliases into {formal_file}")

if __name__ == "__main__":
    execute_merge_simple()
