import os
import json
import yaml

members_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
entity_map_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"

def get_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]), parts[2]
    return {}, content

def save_frontmatter(data, body):
    # Use yaml to dump, but keep it clean
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False)
    return f"---\n{fm}---\n{body}"

def execute_merge():
    with open(entity_map_path, 'r', encoding='utf-8') as f:
        entity_map = json.load(f)

    # Pairs from USER (y/n mapping)
    # y: 小松樹 & いつき
    # y: 山本哲大 & やまもと
    # y: 萩平智之 & HAGI
    # y: 吉崎アキラ & ざき
    # y: 中山佳名子 & 中山
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

        data, body = get_frontmatter(content)
        
        # Update aliases
        existing_aliases = data.get('aliases', [])
        if not isinstance(existing_aliases, list): existing_aliases = [existing_aliases]
        for a in aliases:
            if a not in existing_aliases:
                existing_aliases.append(a)
        data['aliases'] = existing_aliases
        data['last_updated'] = "2026-04-14"

        # Update LOG section with entity data
        all_chats = set()
        total_interactions = 0
        for name in [data.get('name')] + aliases:
            if name in entity_map:
                all_chats.update(entity_map[name]['chats'])
                total_interactions += entity_map[name]['interactions']

        depth_section = f"\n## 📜 LINEログからの知見 (Relation Analysis)\n> [!TIP] 関係性の推定\n> - **主要な呼び名**: {', '.join(aliases)}\n> - **確認済み交流**: {total_interactions}件のログメッセージ\n> - **主要チャット**: {', '.join(list(all_chats)[:5])}など\n"
        
        if 'LINEログからの知見' in body:
            # Replace existing
            import re
            body = re.sub(r'## 📜 LINEログからの知見 \(Relation Analysis\).*?(\n##|$)', depth_section + r'\1', body, flags=re.DOTALL)
        else:
            body = body.replace('## 📝 ログ', depth_section + '\n## 📝 ログ')

        new_content = save_frontmatter(data, body)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Merged aliases into {formal_file}")

if __name__ == "__main__":
    execute_merge()
