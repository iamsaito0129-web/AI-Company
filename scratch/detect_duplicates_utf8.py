import json
import re
from collections import defaultdict

input_file = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"
output_report = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\duplicate_report.md"

def detect_duplicates():
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    normalized_to_names = defaultdict(list)
    for name, info in data.items():
        if info['interactions'] < 2: continue
        # Normalize: keep only kanji/kana
        norm = info['normalized']
        if norm:
            normalized_to_names[norm].append(name)
        
    all_names = sorted([n for n in data.keys() if data[n]['interactions'] > 1], key=len, reverse=True)
    processed = set()
    
    report = ["# 同一人物の可能性がある候補リスト\n", "誕生日や所属、名前の類似性から抽出しました。y/nで教えてください。\n"]
    
    report.append("## 1. 正規化名が一致 (表記揺れ)")
    for norm, names in normalized_to_names.items():
        if len(names) > 1:
            report.append(f"- [ ] **{norm}**: {' / '.join(names)}")
            
    report.append("\n## 2. 包含関係・通称 (ニックネーム)")
    for i, name1 in enumerate(all_names):
        for name2 in all_names[i+1:]:
            # Ignore messages canceled
            if '取消' in name1 or '取消' in name2: continue
            
            # Substring match (e.g. 小松樹 and いつき / although いつき is not in 小松樹 literally, we need a smarter way)
            # For now, literal substring
            if name2 in name1 and len(name2) >= 2:
                report.append(f"- [ ] **{name1}** と **{name2}**")

    # Manual heuristics based on known data
    manual_checks = [
        "- [ ] **小松樹** と **いつき** (学校教育 いつき)",
        "- [ ] **小川美優** と **みゆ** (心優)",
        "- [ ] **清川愛心** と **iroha** (彩華)",
        "- [ ] **山本哲大** と **やまもと**",
        "- [ ] **萩平智之** と **HAGI**",
        "- [ ] **吉崎アキラ** と **ざき**",
        "- [ ] **中山佳名子** と **中山**",
    ]
    report.append("\n## 3. 重要プロジェクトメンバー (手動推定)")
    report.extend(manual_checks)

    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

if __name__ == "__main__":
    detect_duplicates()
