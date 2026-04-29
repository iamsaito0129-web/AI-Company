import os
import yaml

def fix_yaml():
    logs_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
    log_files = [f for f in os.listdir(logs_dir) if f.startswith('[整理済み]') and f.endswith('.md')]

    for filename in log_files:
        file_path = os.path.join(logs_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---')
        if len(parts) < 3: continue
        
        frontmatter = yaml.safe_load(parts[1])
        
        # '発言者' セクションがある場合、それを 'speakers' に移管
        if '発言者' in frontmatter:
            frontmatter['speakers'] = frontmatter['発言者']
            del frontmatter['発言者']
        
        # 修正版を書き出し
        new_content = "---\n" + yaml.dump(frontmatter, allow_unicode=True, sort_keys=False) + "---\n" + '---'.join(parts[2:])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    fix_yaml()
