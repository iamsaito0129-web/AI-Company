import os

def update_miyu():
    path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\小川美優.md"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add relationship depth
    new_relation = """
## 📜 LINEログからの知見 (Relation Analysis)
> [!TIP] 関係性の詳細
> - **愛称**: みゆ, 心優
> - **役割**: PA担当（音響・照明）。オーナーからの信頼が厚く、神霜祭などの大規模イベントでは「ステージ番」としてイレギュラーな事態にも的確に対応する。
> - **交流頻度**: 非常に高く、実委・PA関連のグループで頻繁に連携している。
"""
    if 'LINEログからの知見' not in content:
        content = content.replace('## 📝 ログ', new_relation + '\n## 📝 ログ')
        content = content.replace('last_updated: "2026-04-04"', 'last_updated: "2026-04-14"')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("Updated 小川美優.md")

def update_itsuki():
    path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\小松樹.md"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_relation = """
## 📜 LINEログからの知見 (Relation Analysis)
> [!TIP] 関係性の詳細
> - **愛称**: いつき, 学校教育 いつき
> - **役割**: オーナーの右腕的な存在。PA副長（または代行）として、会議の進行や重要資料の作成を担当。
> - **スキル**: 指導案の作成や会議資料の校閲を得意とし、Sound☆Sproutではパフォーマンスも行う多才な人物。
> - **交流頻度**: オーナーとの連携回数が最も多いメンバーの一人。
"""
    if 'LINEログからの知見' not in content:
        content = content.replace('## 📝 ログ', new_relation + '\n## 📝 ログ')
        content = content.replace('last_updated: "2026-04-04"', 'last_updated: "2026-04-14"')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("Updated 小松樹.md")

if __name__ == "__main__":
    update_miyu()
    update_itsuki()
