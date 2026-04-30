import re

def fix_regex_table_v3():
    file_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"
    
    # ユーザーが入力したC列の生データを取得するために、直前の履歴にある情報を元に
    # ファイル全体を一度文字列として読み込み、正規表現パターン部分を特定します。
    with open(file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # テーブル部分を抽出
    lines = full_text.splitlines()
    header = lines[:7]
    
    # テーブル行の再解析
    # A列(表示名)をキーにして保持
    raw_table_data = []
    for i in range(7, len(lines)):
        line = lines[i].strip()
        if not line.startswith('|'): continue
        if ":---" in line or "A列" in line: continue
        
        parts = [p.strip() for p in line.split('|')]
        # | (empty) | A | B | C | (empty)  のような構造を想定
        # または | A | B | C |
        if len(parts) >= 3:
            # 有効なデータを抽出 (空の要素を除去しつつ)
            actual_data = [p for p in parts if p]
            if len(actual_data) >= 2:
                # A列, B列を抽出
                a_col = actual_data[0]
                b_col = actual_data[1]
                raw_table_data.append([a_col, b_col])
    
    print(f"Detected {len(raw_table_data)} valid rows in original table.")

    # C列の正規表現リスト（以前のスクリプトで混入した可能性のあるテーブル行を除去し、純粋なリストを取得）
    # ユーザーが「テキストで入力している」と言及した部分
    # すでに一度上書きしてしまったため、現在のファイルから「^...$」のパターンのみを抽出
    all_regex = re.findall(r'^\^.+$', full_text, re.MULTILINE)
    
    # もしfindallで取れない場合、前回の実行でテーブルの中に埋め込まれたものを抽出
    if len(all_regex) < 100:
        all_regex = []
        for line in lines:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and parts[3].startswith('^'):
                all_regex.append(parts[3])

    print(f"Extracted {len(all_regex)} regex patterns.")

    # テーブルの再構成
    new_lines = ["".join(header)]
    # headerに改行が含まれていない場合の調整
    if not new_lines[0].endswith('\n'): new_lines[0] += '\n'
    
    for i in range(len(raw_table_data)):
        a_col, b_col = raw_table_data[i]
        c_col = all_regex[i] if i < len(all_regex) else ""
        new_lines.append(f"| {a_col} | {b_col} | {c_col} |")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines) + "\n")
    
    print("Table re-constructed correctly.")

if __name__ == "__main__":
    fix_regex_table_v3()
