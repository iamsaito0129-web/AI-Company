import os
import re
import yaml
import shutil
from pathlib import Path

# パス設定
BASE_DIR = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
CHUNK_SIZE = 30

def extract_frontmatter(content):
    """YAMLフロントマッターを抽出する"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)), match.end()
        except yaml.YAMLError:
            return None, 0
    return None, 0

def split_into_chunks(content):
    """
    メッセージ行を30件ずつの塊に分割する。
    行の形式: "- **HH:mm [[名前]]**： メッセージ" または "## YYYY.MM.DD"
    """
    lines = content.splitlines()
    chunks = []
    current_chunk = []
    message_count = 0
    
    # 日付ヘッダーを保持するための変数
    last_date_header = ""

    for line in lines:
        # メッセージ行かどうか判定
        if re.match(r'^- \*\*.*\*\*：', line):
            current_chunk.append(line)
            message_count += 1
        elif line.startswith("## "):
            last_date_header = line
            current_chunk.append(line)
        else:
            # それ以外の行（概要や空行など）は無視するか、適切に処理
            if line.strip():
                current_chunk.append(line)

        if message_count >= CHUNK_SIZE:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            if last_date_header:
                current_chunk.append(last_date_header)
            message_count = 0
            
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks

def summarize_chunk(chunk_content):
    """
    チャンクを要約する。
    ※ 実際にはAIによる要約が必要ですが、スクリプト内では構造化された抜粋を作成します。
    ※ 要件では「損失をなくして」とあるため、要約というよりは「圧縮された記録」として全情報を保持しつつ簡潔にします。
    """
    # ここではシンプルに、各発言の要点（またはそのまま）をまとめる形式にします。
    # 実際にはこの後、モデルがこのスクリプトの結果を見て「本物の要約」を行うプロセスになりますが、
    # スクリプトとしては「チャンクごとのセクション」を作成することに主眼を置きます。
    
    summary = "### 要約ユニット\n"
    summary += chunk_content
    return summary

def process_files():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    files = [f for f in os.listdir(BASE_DIR) if f.startswith("【整理済み】") and f.endswith(".md")]

    for filename in files:
        file_path = os.path.join(BASE_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body_start = extract_frontmatter(content)
        if not frontmatter:
            print(f"Skip {filename}: No frontmatter")
            continue

        body = content[body_start:]
        
        # チャンク分割
        chunks = split_into_chunks(body)
        
        # 要約済みファイルの内容作成
        summary_filename = filename.replace("【整理済み】", "【要約済み】")
        summary_file_path = os.path.join(BASE_DIR, summary_filename)
        
        # フロントマッターの更新
        new_frontmatter = frontmatter.copy()
        new_frontmatter['type'] = 'line_summary'
        new_frontmatter['status'] = '要約済み'
        # 整備済みファイルへのリンクを追加（アーカイブ後のパスを想定）
        rel_archive_path = f"[[archive/{filename}]]"
        new_frontmatter['source_log'] = rel_archive_path
        
        summary_content = "---\n"
        summary_content += yaml.dump(new_frontmatter, allow_unicode=True)
        summary_content += "---\n\n"
        summary_content += f"# {summary_filename.replace('.md', '')}\n\n"
        summary_content += f"元ログ: {rel_archive_path}\n\n"
        
        for i, chunk in enumerate(chunks):
            summary_content += f"## チャンク {i+1}\n"
            summary_content += chunk + "\n\n"

        # 要約済みファイルの書き出し
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
            
        # 元ファイルのフロントマッターに要約済みへのリンクを追加
        frontmatter['summary_link'] = f"[[{summary_filename}]]"
        updated_original = "---\n"
        updated_original += yaml.dump(frontmatter, allow_unicode=True)
        updated_original += "---\n"
        updated_original += body
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_original)

        # アーカイブへ移動
        shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
        try:
            print(f"Processed: {filename}")
        except UnicodeEncodeError:
            print(f"Processed a file (encoding issue in print)")

if __name__ == "__main__":
    process_files()
