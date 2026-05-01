import os
import glob
import re
import csv

md_dir = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
mapping_file = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"
out_csv = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\unknown_line_names.csv"

def get_official_names():
    official = set()
    if not os.path.exists(mapping_file):
        return official
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    c_col = parts[3]
                    if c_col and c_col not in ["C列用(正規名)", "---", "名前が不足"]:
                        official.add(c_col)
    return official

def extract_unknown():
    official_names = get_official_names()
    files = glob.glob(os.path.join(md_dir, '*.md'))
    
    unknown_names = set()
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            in_yaml = False
            for line in f:
                line = line.strip()
                if line == "---":
                    if not in_yaml:
                        in_yaml = True
                    else:
                        break # yaml ends
                elif in_yaml and line.startswith("- "):
                    speaker = line[2:].strip()
                    if speaker and speaker not in official_names and speaker != "名前が不足":
                        unknown_names.add(speaker)
    
    # 簡単なマッピング推測（C列の部分一致など）
    suggestions = {}
    for unk in unknown_names:
        sugg = ""
        # official_namesのどれかに含まれるか、逆に含まれるか
        for off in official_names:
            if off in unk or unk in off:
                sugg = off
                break
        suggestions[unk] = sugg
        
    # csv書き出し
    with open(out_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["元のLINE名", "提案される正規名(C列用)"])
        for unk in sorted(unknown_names):
            writer.writerow([unk, suggestions[unk]])

if __name__ == "__main__":
    extract_unknown()
    print("CSV updated.")
