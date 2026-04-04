# -*- coding: utf-8 -*-
import os

members = [
    {"name": "中川陽登", "bday": "2003-09-24", "age": 22, "base": "田辺・美章園・文の里"},
    {"name": "松本悠里", "bday": "2003-08-13", "age": 22, "base": ""},
    {"name": "小松樹", "bday": "2003-10-29", "age": 22, "base": "六甲アイランド"},
    {"name": "反田淳平", "bday": "2004-02-21", "age": 22, "base": "久宝寺・久宝寺口"},
    {"name": "前田紗映", "bday": "2003-06-18", "age": 22, "base": "河内国分・高井田"},
    {"name": "國貞史華", "bday": "2003-04-14", "age": 22, "base": "昭和町・文の里"},
    {"name": "田上優希", "bday": "2003-07-05", "age": 22, "base": "豊中"},
    {"name": "三宅莉瑠", "bday": "2004-02-12", "age": 22, "base": "高槻"},
    {"name": "毛穴大翔", "bday": "2002-08-29", "age": 23, "base": "河内山本"},
    {"name": "花本萌々子", "bday": "2003-11-03", "age": 22, "base": "京橋？"},
    {"name": "新谷柊太", "bday": "2004-02-03", "age": 22, "base": "布施・今里"},
    {"name": "中山佳名子", "bday": "2005-03-08", "age": 21, "base": "住之江"},
    {"name": "萩平智之", "bday": "", "age": 0, "base": "宝塚"},
    {"name": "粂咲帆", "bday": "2004-12-07", "age": 21, "base": "豊中"},
    {"name": "山本哲大", "bday": "2004-08-01", "age": 21, "base": "寝屋川"},
    {"name": "吉崎アキラ", "bday": "2004-09-23", "age": 21, "base": ""},
    {"name": "清川愛心", "bday": "2005-02-13", "age": 21, "base": "西明石"},
    {"name": "青木菜直", "bday": "2004-08-17", "age": 21, "base": ""},
    {"name": "小川美優", "bday": "2005-03-17", "age": 21, "base": "国分"}
]

output_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\hr\members"

template = """---
name: "{name}"
category: "{category}"
community: "大学祭実行委員会"
tags: ["{age}歳", "{base}", "大学祭実行委員会", "{category}"]
last_updated: "2026-04-04"
birthday: "{bday_short}"
age: {age}
base: "{base}"
cssclasses: ["profile-card"]
---

# 👤 {name}

> [!ABSTRACT] プロファイル要約
> **【大学祭実行委員会 {category}】**
> オーナーの学生時代の活動を共にしたメンバー。

## 💎 スキル / 特性 (Obsidian-Skills)
- **現在の年齢**: {age}歳 ({year}年生まれ)
- **コミュニティ**: 大学祭実行委員会
- **活動拠点**: {base}

## 📖 関係性の歴史
- **出会い**: 大学祭実行委員会
- **時代**: 学生時代 (同期・後輩)

## 🔗 ネットワーク (Mermaid)
```mermaid
graph LR
    Owner((オーナー)) <--> |{category}| Member[({name})]
    Member --- Community[大学祭実行委員会]
    Member --- Base[({base})]
```

## 📝 ログ
- **2026-04-04**: メンバーリストより一括登録実施。
"""

for m in members:
    # 22歳付近を同期、それ以外を後輩/先輩と判定
    if m["age"] == 22:
        category = "同期"
    elif m["age"] == 21:
        category = "後輩"
    elif m["age"] == 23:
        category = "先輩"
    else:
        category = "メンバー"
        
    year = m["bday"][:4] if m["bday"] else "不明"
    bday_short = m["bday"][5:] if m["bday"] else ""
    
    file_content = template.format(
        name=m["name"],
        category=category,
        age=m["age"],
        base=m["base"] if m["base"] else "不明",
        bday_short=bday_short,
        year=year
    )
    
    file_path = os.path.join(output_dir, f"{m['name']}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

print(f"Successfully created {len(members)} files.")
