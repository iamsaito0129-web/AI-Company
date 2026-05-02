import os
import yaml
import re
from datetime import datetime

MEMBER_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"

def get_tag_recommendations(data, body):
    tags = set()
    
    # 1. 関係性 (#rel/)
    category = str(data.get("category", ""))
    if "家族" in category: tags.add("#rel/family")
    elif "親戚" in category: tags.add("#rel/relative")
    elif "親友" in category: tags.add("#rel/bestie")
    elif "友人" in category: tags.add("#rel/friend")
    elif "後輩" in category: tags.add("#rel/junior")
    elif "先輩" in category: tags.add("#rel/senior")
    elif "教員" in category or "同僚" in category or "仕事" in category: tags.add("#rel/colleague")
    elif "教え子" in category: tags.add("#rel/student")
    
    # 2. 所属 (#org/)
    communities = data.get("community", [])
    if not isinstance(communities, list): communities = [communities]
    communities_str = " ".join([str(c) for c in communities])
    
    if any(k in communities_str or k in category for k in ["大学祭", "実委", "学祭"]): tags.add("#org/festival-staff")
    if any(k in communities_str or k in category for k in ["たこ", "地域", "地元"]): tags.add("#org/local-event")
    if any(k in communities_str or k in category for k in ["大学", "院"]): tags.add("#org/univ")
    if any(k in communities_str or k in category for k in ["学校", "職場", "校"]): tags.add("#org/school")
    if any(k in communities_str or k in category for k in ["幼馴染", "中学", "高校", "小学校"]): tags.add("#org/childhood")
    
    # 3. 状態 (#status/)
    last_contact = data.get("last_contact_line")
    vip = data.get("vip", False)
    if vip: tags.add("#status/vip")
    
    if last_contact:
        try:
            lc_date = datetime.strptime(last_contact, "%Y-%m-%d")
            months_diff = (datetime.now() - lc_date).days / 30
            if months_diff < 3:
                tags.add("#status/active")
            elif months_diff < 12:
                tags.add("#status/dormant")
                tags.add("#type/needs-catchup")
            else:
                tags.add("#status/dormant")
        except:
            pass
    else:
        tags.add("#status/lost-touch")
        
    # 4. 興味・関心 (#interest/) - キーワード検知
    full_text = str(data) + body
    if any(k in full_text for k in ["酒", "飲み", "ビール", "ワイン", "日本酒", "バー"]): tags.add("#interest/liquor")
    if any(k in full_text for k in ["教育", "先生", "学校", "授業", "学習"]): tags.add("#interest/edu")
    if any(k in full_text for k in ["ガジェット", "IT", "AI", "エンジニア"]) or re.search(r"プログラム(?!シート)", full_text): tags.add("#interest/tech")
    if any(k in full_text for k in ["デザイン", "写真", "アート", "絵", "クリエイティブ"]): tags.add("#interest/art")
    if any(k in full_text for k in ["グルメ", "食べ歩き", "料理", "美味しい", "レストラン"]): tags.add("#interest/foodie")
    if any(k in full_text for k in ["スポーツ", "野球", "サッカー", "キャンプ", "アウトドア"]): tags.add("#interest/sports")
    
    # 5. 運用 (#type/)
    if "卒論" in full_text: tags.add("#type/grad-thesis")
    if not data.get("line_names") or "{{プレースホルダー}}" in body: tags.add("#type/input-pending")
    
    return sorted(list(tags))

def process_members():
    updated_count = 0
    for f in os.listdir(MEMBER_DIR):
        if not f.endswith(".md") or f.startswith("_"): continue
        path = os.path.join(MEMBER_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 2: continue
            data = yaml.safe_load(parts[1])
            if not data or "name" not in data: continue
            
            body = parts[2] if len(parts) > 2 else ""
            
            # タグ生成
            new_tags = get_tag_recommendations(data, body)
            
            if new_tags:
                # 既存のタグと統合（重複削除）
                existing_tags = data.get("tags", [])
                if not isinstance(existing_tags, list): existing_tags = [existing_tags]
                # 全て新体系に置き換えるか、統合するか？
                # ユーザーは「整理する」と言ったので、今回は新体系を優先して上書き/整理する
                data["tags"] = new_tags
                
                new_frontmatter = yaml.dump(data, allow_unicode=True, sort_keys=False).strip()
                new_content = f"---\n{new_frontmatter}\n---" + body
                
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                updated_count += 1
                
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    print(f"Finished tagging {updated_count} members.")

if __name__ == "__main__":
    process_members()
