import os
import re
from datetime import datetime

members_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members"
current_date = datetime(2026, 4, 14)

def update_birth_years():
    for filename in os.listdir(members_dir):
        if not filename.endswith('.md') or filename.startswith('_'): continue
        path = os.path.join(members_dir, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract age and birthday (MM-DD)
        age_match = re.search(r'age:\s*(\d+)', content)
        birthday_match = re.search(r'birthday:\s*"?(\d{2})-(\d{2})"?', content)
        
        if age_match and birthday_match:
            age = int(age_match.group(1))
            b_month = int(birthday_match.group(1))
            b_day = int(birthday_match.group(2))
            
            # Calculate birth year
            # age as of 2026-04-14
            birth_year = 2026 - age
            if (b_month, b_day) > (4, 14):
                birth_year -= 1
            
            # Update birthday property to YYYY-MM-DD
            new_birthday = f"{birth_year}-{b_month:02d}-{b_day:02d}"
            
            # Replace birthday: MM-DD with birthday: YYYY-MM-DD
            content = re.sub(r'birthday:\s*"?\d{2}-\d{2}"?', f'birthday: "{new_birthday}"', content)
            
            # Update text description if exists (e.g. "22歳 (2003年生まれ)")
            content = re.sub(r'(\d+)歳\s*\(\d+年生まれ\)', f'\\1歳 ({birth_year}年生まれ)', content)
            # If no year in text yet, add it
            def repl_year(m):
                a = m.group(1)
                return f"{a}歳 ({birth_year}年生まれ)"
            
            if "年生まれ" not in content:
                content = re.sub(r'(\d+)歳', repl_year, content)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename} to birthday: {new_birthday}")

if __name__ == "__main__":
    update_birth_years()
