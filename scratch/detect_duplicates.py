import json
import re
from collections import defaultdict

input_file = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"

def detect_duplicates():
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    normalized_to_names = defaultdict(list)
    for name, info in data.items():
        # Optimization: ignore messages from system or generic names if any
        if info['interactions'] < 2: continue
        normalized_to_names[info['normalized']].append(name)
        
    # Potential candidates
    candidates = []
    for norm, names in normalized_to_names.items():
        if len(names) > 1:
            candidates.append({"normalized": norm, "variants": names})
            
    # Fuzzy or manual matching logic
    # Example: "いつき" and "小松樹"
    # Actually, we can check if a name is a substring of another
    all_names = sorted(data.keys(), key=len, reverse=True)
    processed = set()
    
    fringe_candidates = []
    for i, name1 in enumerate(all_names):
        if name1 in processed: continue
        for name2 in all_names[i+1:]:
            if name2 in processed: continue
            # If name2 is a common nickname or first name of name1
            if name2 in name1 and len(name2) >= 2:
                fringe_candidates.append({"primary": name1, "alias": name2})
    
    return candidates, fringe_candidates

if __name__ == "__main__":
    candidates, fringe = detect_duplicates()
    print("### 同一人物の可能性がある候補リスト")
    print("\n#### パターンA: 正規化名が一致")
    for c in candidates:
        print(f"- **{c['normalized']}**: {' / '.join(c['variants'])}")
        
    print("\n#### パターンB: 名前に包含関係あり")
    for f in fringe:
        print(f"- **{f['primary']}** と **{f['alias']}**")
