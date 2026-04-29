import os
import re
import json
import yaml

def finalize_logs():
    map_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\final_conversion_map.json"
    logs_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
    
    with open(map_path, 'r', encoding='utf-8') as f:
        conversion_map = json.load(f)

    # ログファイルのリスト取得 ([整理済み]*.md)
    log_files = [f for f in os.listdir(logs_dir) if f.startswith('[整理済み]') and f.endswith('.md')]

    for filename in log_files:
        file_path = os.path.join(logs_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # YAMLと本文を分離
        parts = content.split('---')
        if len(parts) < 3: continue
        
        frontmatter = yaml.safe_load(parts[1])
        body = '---'.join(parts[2:])

        # 1. YAMLの speakers を更新
        old_speakers = frontmatter.get('speakers', [])
        new_speakers = sorted(list(set([conversion_map.get(s, s) for s in old_speakers])))
        frontmatter['speakers'] = new_speakers

        # 2. 本文の発言者名を一括置換
        # パターン: "HH:MM [表示名] "
        # 前回の整理で "HH:MM 名前 " という形式にしている
        def replace_speaker(match):
            time_part = match.group(1)
            old_name = match.group(2)
            new_name = conversion_map.get(old_name, old_name)
            return f"{time_part} {new_name} "

        # 置換実行
        # 正規表現: (\d{2}:\d{2})\s+(.+?)\s
        # 注意: 名前の後のスペースまでマッチさせる
        new_body = re.sub(r'(\d{2}:\d{2})\s+(.+?)\s', replace_speaker, body)

        # 3. 統計情報の更新 (任意だが、今回は整合性のため)
        # 発言回数などを再集計しても良いが、一旦名前の置換を優先

        # ファイル書き戻し
        new_content = "---\n" + yaml.dump(frontmatter, allow_unicode=True) + "---\n" + new_body
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print(f"Processed {len(log_files)} files.")

if __name__ == "__main__":
    finalize_logs()
