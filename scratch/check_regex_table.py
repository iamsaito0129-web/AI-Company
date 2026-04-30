import re
import os

BASE_DIR = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company"
REGEX_FILE = os.path.join(BASE_DIR, "company", "hr", "members", "line_name_regex.md")

def check_table():
    with open(REGEX_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    table_started = False
    for i, line in enumerate(lines):
        line = line.strip()
        if "|" in line and "A列" in line:
            table_started = True
            continue
        if table_started and line.startswith("| :---"):
            continue
        if table_started and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                a_col = parts[1]
                c_col = parts[3]
                if "名前が不足" in c_col:
                    # If A column has multiple words or long name, it might be a mistake
                    print(f"Line {i+1}: A='{a_col}' -> C='{c_col}'")

if __name__ == "__main__":
    check_table()
