import os
import re

members_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"

def generate_birthday_table():
    members = []
    for filename in os.listdir(members_dir):
        if not filename.endswith('.md') or filename.startswith('_'): continue
        path = os.path.join(members_dir, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        name_match = re.search(r'name:\s*"(.*?)"', content)
        bday_match = re.search(r'birthday:\s*"?(\d{4})-(\d{2})-(\d{2})"?', content)
        if not bday_match:
            # Try old format just in case
            bday_match = re.search(r'birthday:\s*"?(\d{2})-(\d{2})"?', content)
            
        if name_match and bday_match:
            name = name_match.group(1)
            if len(bday_match.groups()) == 3:
                year, month, day = bday_match.groups()
                members.append({"name": name, "month": month, "day": day, "year": year})
            else:
                month, day = bday_match.groups()
                members.append({"name": name, "month": month, "day": day, "year": "????"})
                
    # Sort by month then day
    members.sort(key=lambda x: (x['month'], x['day']))
    
    print("| 名前 | 誕生日 | 生年 |")
    print("| :--- | :--- | :--- |")
    for m in members:
        print(f"| [[{m['name']}]] | {m['month']}-{m['day']} | {m['year']} |")

if __name__ == "__main__":
    generate_birthday_table()
