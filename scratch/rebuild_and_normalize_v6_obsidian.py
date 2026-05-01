import os
import glob
import re
from datetime import datetime

archive_dir = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs\archive"
output_dir = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
mapping_file = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"

def parse_mapping():
    mapping = {}
    if not os.path.exists(mapping_file):
        return mapping
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    raw_name = parts[1]
                    canon_name = parts[3]
                    if raw_name and raw_name != "元のLINE名" and raw_name != "---":
                        mapping[raw_name] = canon_name if canon_name else "名前が不足"
    return mapping

def process_logs():
    mapping = parse_mapping()
    name_keys = sorted(mapping.keys(), key=len, reverse=True)
    
    files = glob.glob(os.path.join(archive_dir, '*.txt'))
    
    sys_patterns = [
        (re.compile(r'^(.*?)(が)?メッセージの送信を取り消しました$'), "メッセージの送信を取り消しました"),
        (re.compile(r'^(.*?)(が)?退出しました。$'), "退出しました。"),
        (re.compile(r'^(.*?)(が)?グループに参加しました。$'), "グループに参加しました。"),
        (re.compile(r'^(.*?)(が)?(.+)をグループに追加しました。$'), "をグループに追加しました。"),
        (re.compile(r'^(.*?)(が)?招待をキャンセルしました。$'), "招待をキャンセルしました。")
    ]
    
    for fpath in files:
        fname = os.path.basename(fpath)
        out_name = fname.replace('.txt', '.md').replace('[済]', '[整理済み]')
        out_path = os.path.join(output_dir, out_name)
        
        unique_speakers = set()
        parsed_lines = []
        dates = []
        
        with open(fpath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line: continue
                
                # 日付行の判定
                date_match = re.match(r'^(\d{4})[\./](\d{2})[\./](\d{2})', line)
                if date_match and ("曜日" in line or "(" in line):
                    y, m, d = date_match.groups()
                    dates.append(f"{y}-{m}-{d}")
                    parsed_lines.append(f"## {line}")
                    continue
                    
                match = re.match(r'^(\d{2}:\d{2})\s+(.+)$', line)
                if match:
                    time_str = match.group(1)
                    rest = match.group(2)
                    speaker_raw = None
                    message = ""
                    is_sys = False
                    
                    for p, msg_template in sys_patterns:
                        m_sys = p.match(rest)
                        if m_sys:
                            speaker_raw = m_sys.group(1).strip()
                            if msg_template == "をグループに追加しました。":
                                target = m_sys.group(3)
                                message = f"*{target} をグループに追加しました。*"
                            else:
                                message = f"*{msg_template}*"
                            is_sys = True
                            break
                    
                    if not is_sys:
                        found = False
                        for nk in name_keys:
                            if rest.startswith(nk):
                                after_nk = rest[len(nk):]
                                if after_nk == "" or after_nk[0] in ['\t', ' ', '　']:
                                    speaker_raw = nk
                                    message = after_nk.lstrip('\t 　')
                                    found = True
                                    break
                        if not found:
                            space_idx = rest.find('\t')
                            if space_idx == -1: space_idx = rest.find(' ')
                            if space_idx != -1:
                                speaker_raw = rest[:space_idx]
                                message = rest[space_idx+1:].lstrip('\t 　')
                            else:
                                speaker_raw = None
                                message = rest

                    reg_name = None
                    if speaker_raw:
                        reg_name = mapping.get(speaker_raw, speaker_raw)
                        if reg_name != "名前が不足" and reg_name:
                            unique_speakers.add(reg_name)
                    
                    if reg_name and reg_name != "名前が不足":
                        parsed_lines.append(f"- **{time_str} [[{reg_name}]]**： {message}")
                    else:
                        parsed_lines.append(f"- **{time_str}**： {message}")
                else:
                    parsed_lines.append(line)
        
        # YAMLプロパティの構築
        start_date = min(dates) if dates else "不明"
        end_date = max(dates) if dates else "不明"
        
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write("---\n")
            out_f.write("type: line_log\n")
            out_f.write(f"title: \"{fname.replace('.txt', '')}\"\n")
            out_f.write(f"date_range: {start_date} to {end_date}\n")
            out_f.write("speakers:\n")
            for s in sorted(unique_speakers):
                out_f.write(f"  - \"[[{s}]]\"\n")
            out_f.write("status: 整理済み\n")
            out_f.write("tags:\n")
            out_f.write("  - line_log\n")
            out_f.write("---\n\n")
            out_f.write(f"# {fname.replace('.txt', '')}\n\n")
            out_f.write(f"> [!INFO] ログ概要\n")
            out_f.write(f"> - **期間**: {start_date} 〜 {end_date}\n")
            out_f.write(f"> - **参加者**: {', '.join(['[['+s+']]' for s in sorted(unique_speakers)])}\n\n")
            for p_line in parsed_lines:
                out_f.write(p_line + "\n")

if __name__ == "__main__":
    process_logs()
    print("Obsidian-optimized log rebuilding complete.")
