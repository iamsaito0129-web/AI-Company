import os
import re

members_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members'

name_map = {
    'あずまさな': ('東紗菜', '222201'),
    'あま': ('天川敬太郎', '222202'),
    'しだことね': ('石田琴音', '222203'), # Grep result was 'いしだことね' but let's be careful
    'いしだことね': ('石田琴音', '222203'),
    'いなばちえ': ('稲葉千恵', '222204'),
    'すじもとまなみ': ('辻本真菜実', '222214'),
    'たくや': ('桂拓也', '222208'),
    'ともみ': ('旨森智美', '222223'),
    'なつき': ('西村夏輝', '222217'),
    'にしだかりね': ('西田香鈴音', '222216'),
    'はしきょー': ('橋本京佳', '222218'),
    'けいちゃん': ('林慶太朗', '222219'),
    'ななせ': ('藤澤七彩', '222220'),
    'まこ': ('山崎真琴', '222224'),
    'わかんばやしちひろ': ('若林千紘', '222226'),
    'わたなべそら': ('渡邊青空', '222227'),
    'Tりょーや': ('田村怜也', '222212'),
    'Yりょーや': ('山本涼矢', '222225')
}

def process_integration(nickname, fullname, student_id):
    nick_path = os.path.join(members_dir, f'{nickname}.md')
    full_path = os.path.join(members_dir, f'{fullname}.md')
    
    if os.path.exists(nick_path):
        with open(nick_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = content.replace(f'name: "{nickname}"', f'name: "{fullname}"')
        
        # Add student_id after the first ---
        if 'student_id:' not in content:
            content = content.replace('---', f'---\nstudent_id: "{student_id}"', 1)
            
        # Add alias
        if 'aliases:' not in content:
            content = content.replace('name:', f'aliases: ["{nickname}"]\nname:')
        else:
            if f'"{nickname}"' not in content:
                content = re.sub(r'aliases: \[(.*?)\]', r'aliases: [\1, "' + nickname + '"]', content)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        os.remove(nick_path)
        print(f'Processed {nickname} -> {fullname}')

# 1. confirmed integrations
process_integration('いっちゃん', '小松樹', '222211')
process_integration('まっちゃん', '松本悠里', '222222')

# 2. Roster mapping
for nick, (full, sid) in name_map.items():
    process_integration(nick, full, sid)

# 3. Sabuchan -> Otani Saburo
sabuchan_path = os.path.join(members_dir, 'さぶちゃん.md')
osaburo_path = os.path.join(members_dir, '大谷三郎.md')
if os.path.exists(sabuchan_path):
    with open(sabuchan_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('name: "さぶちゃん"', 'name: "大谷三郎"')
    content = content.replace('category: "友人"', 'category: "家族"')
    if 'aliases:' not in content:
        content = content.replace('name:', 'aliases: ["さぶちゃん"]\nname:')
    else:
        content = re.sub(r'aliases: \[(.*?)\]', r'aliases: [\1, "さぶちゃん"]', content)
    with open(osaburo_path, 'w', encoding='utf-8') as f:
        f.write(content)
    os.remove(sabuchan_path)
    print('Processed さぶちゃん -> 大谷三郎')
