import os
import glob
import re

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
                        # C列が空の場合は「名前が不足」として扱う
                        mapping[raw_name] = canon_name if canon_name else "名前が不足"
    return mapping

def process_logs():
    mapping = parse_mapping()
    # 長い名前順にソート（前方一致での誤爆を防ぐため）
    name_keys = sorted(mapping.keys(), key=len, reverse=True)
    
    files = glob.glob(os.path.join(archive_dir, '*.txt'))
    
    # システムメッセージのパターン定義
    sys_patterns = [
        (re.compile(r'^(.*?)(が)?メッセージの送信を取り消しました$'), "メッセージの送信を取り消しました"),
        (re.compile(r'^(.*?)(が)?退出しました。$'), "退出しました。"),
        (re.compile(r'^(.*?)(が)?グループに参加しました。$'), "グループに参加しました。"),
        (re.compile(r'^(.*?)(が)?(.+)をグループに追加しました。$'), "をグループに追加しました。"), # ちょっと特殊なので後で処理
        (re.compile(r'^(.*?)(が)?招待をキャンセルしました。$'), "招待をキャンセルしました。")
    ]
    
    for fpath in files:
        fname = os.path.basename(fpath)
        out_name = fname.replace('.txt', '.md').replace('[済]', '[整理済み]')
        out_path = os.path.join(output_dir, out_name)
        
        unique_speakers = set()
        parsed_lines = []
        
        with open(fpath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                
                # 日付行の判定 (例: 2025.11.02 日曜日)
                if re.match(r'^\d{4}\.\d{2}\.\d{2}\s+.*?曜日$', line) or re.match(r'^\d{4}/\d{2}/\d{2}\(.*?$', line):
                    parsed_lines.append(f"## {line}")
                    continue
                    
                # 時間行の判定
                match = re.match(r'^(\d{2}:\d{2})\s+(.+)$', line)
                if match:
                    time_str = match.group(1)
                    rest = match.group(2)
                    
                    speaker_raw = None
                    message = ""
                    
                    # 1. システムメッセージの判定
                    is_sys = False
                    for p, msg_template in sys_patterns:
                        m_sys = p.match(rest)
                        if m_sys:
                            # 抽出された名前部分
                            speaker_raw = m_sys.group(1).strip()
                            if not speaker_raw:
                                speaker_raw = None
                            
                            if msg_template == "をグループに追加しました。":
                                target = m_sys.group(3)
                                message = f"{target} をグループに追加しました。"
                            else:
                                message = msg_template
                                
                            is_sys = True
                            break
                    
                    # 2. 通常メッセージの判定
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
                        
                        # マップに見つからない場合のフォールバック（最初のタブかスペースまでを名前とする）
                        if not found:
                            space_idx = rest.find('\t')
                            if space_idx == -1:
                                space_idx = rest.find(' ')
                            
                            if space_idx != -1:
                                speaker_raw = rest[:space_idx]
                                message = rest[space_idx+1:].lstrip('\t 　')
                            else:
                                # タブもスペースも無い場合は、人名とメッセージの区切りがないため全体をメッセージとする
                                speaker_raw = None
                                message = rest

                    # speaker_raw の正規化と登録
                    reg_name = None
                    if speaker_raw:
                        reg_name = mapping.get(speaker_raw, speaker_raw)
                        if reg_name != "名前が不足" and reg_name:
                            unique_speakers.add(reg_name)
                    
                    # Markdown用に整形
                    if reg_name and reg_name != "名前が不足":
                        parsed_lines.append(f"- **{time_str} {reg_name}**： {message}")
                    else:
                        parsed_lines.append(f"- **{time_str}**： {message}")
                else:
                    # 時間でも日付でもない行は、前のメッセージの続きとして扱う
                    parsed_lines.append(line)
        
        # Markdownファイルへ書き出し
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write("---\n")
            out_f.write("speakers:\n")
            if unique_speakers:
                for s in sorted(unique_speakers):
                    out_f.write(f"  - {s}\n")
            out_f.write("---\n\n")
            out_f.write(f"# {fname.replace('.txt', '')}\n\n")
            for p_line in parsed_lines:
                out_f.write(p_line + "\n")

if __name__ == "__main__":
    process_logs()
    print("Log parsing and rebuilding complete.")
