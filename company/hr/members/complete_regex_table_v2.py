import re

def complete_regex_table():
    file_path = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_name_regex.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # ヘッダーと説明文を保持 (1-7行目)
    header_content = lines[:7]
    
    # 8行目からテーブル行を抽出
    table_rows = []
    text_area_start = 0
    for i in range(7, len(lines)):
        line = lines[i].strip()
        if line.startswith('|'):
            # テーブル行として保持
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                table_rows.append(parts)
        elif line == "C列" or (not line and i > 10):
            # テーブル終了、C列データの開始点を探す
            text_area_start = i
            break
    
    print(f"Found {len(table_rows)} rows in table.")

    # C列データの抽出 (見出し 'C列' 以降の有効な行)
    regex_data = []
    collecting = False
    for i in range(text_area_start, len(lines)):
        line = lines[i].strip()
        if line == "C列":
            collecting = True
            continue
        if collecting and line:
            # ページタイトルなどは除外したいが、基本的には全行取得
            regex_data.append(line)
    
    print(f"Found {len(regex_data)} regex lines in text area.")

    # テーブルの更新
    completed_table = []
    # インデックスに基づいて流し込み
    for i in range(len(table_rows)):
        row = table_rows[i]
        # row[0]は空, row[1]=A列, row[2]=B列, row[3]=C列
        if i < len(regex_data):
            row[3] = regex_data[i]
        else:
            row[3] = "" # データが足りない場合は空
        
        # テーブル行として整形
        formatted_row = f"| {row[1]} | {row[2]} | {row[3]} |"
        completed_table.append(formatted_row)

    # 最終的なファイル内容の構築
    # 元の説明文 + 完成したテーブル + (任意)下部のテキストエリアは削除
    new_content = "".join(header_content)
    new_content += "\n".join(completed_table) + "\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully completed the table in {file_path}")

if __name__ == "__main__":
    complete_regex_table()
