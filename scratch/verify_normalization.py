import os
import re
import yaml

BASE_DIR = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company"
REGEX_FILE = os.path.join(BASE_DIR, "company", "hr", "members", "line_name_regex.md")
LOGS_DIR = os.path.join(BASE_DIR, "company", "hr", "members", "line_logs")

def get_ignored_names(file_path):
    ignored = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line and ("名前が不足" in line):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4 and ("名前が不足" in parts[3]):
                    ignored.add(parts[1])
    return ignored

def verify():
    ignored = get_ignored_names(REGEX_FILE)
    print(f"Checking for ignored names: {ignored}")
    
    files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".md")]
    violations = []
    
    for filename in files:
        filepath = os.path.join(LOGS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        parts = re.split(r"^---$", content, flags=re.MULTILINE)
        if len(parts) < 3: continue
        
        metadata = yaml.safe_load(parts[1])
        speakers = metadata.get('speakers', [])
        appearances = metadata.get('登場人物', [])
        
        for name in ignored:
            if name in speakers:
                violations.append(f"{filename}: '{name}' found in speakers")
            if name in appearances:
                violations.append(f"{filename}: '{name}' found in appearances")
                
    if not violations:
        print("Success: No ignored names found in properties.")
    else:
        print("Violations found:")
        for v in violations:
            print(v)

if __name__ == "__main__":
    verify()
