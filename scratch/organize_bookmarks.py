import re
import os
from bs4 import BeautifulSoup

def process_bookmarks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Netscape bookmark files are not strictly valid HTML, so we use a permissive parser
    # or handle the <DL><p> structure.
    soup = BeautifulSoup(content, 'html.parser')

    # Mapping for renaming based on URL patterns or current names
    rename_map = {
        "https://mail.notion.so/inbox": "Notion Inbox (タスク管理)",
        "https://www.gizmodo.jp/": "Gizmodo (テクノロジーニュース)",
        "https://jetstream.blog/": "Jetstream (ガジェットブログ)",
        "https://gazyekichi96.com/": "Gazyekichi96 (モバイル最新情報)",
        "https://loilonote.app/_/": "ロイロノート (授業支援)",
        "https://store.google.com/jp/": "Google Store (ハードウェア)",
        "https://fast.com/ja/": "FAST.com (スピードテスト)",
        "https://manager.line.biz/": "LINE Official Account (管理)",
        "https://loungegame.site/": "人狼オンライン (娯楽)",
        "https://discord.com/channels/@me": "Discord (コミュニケーション)",
        "https://sites.google.com/new": "Google Sites (ウェブ構築)",
        "https://chat.openai.com/": "ChatGPT (メイン対話AI)",
        "https://claude.ai/": "Claude (高度論理AI)",
        "https://www.chatpdf.com/": "ChatPDF (PDFドキュメント分析)",
        "https://bard.google.com/": "Gemini (Google 検索連動AI)",
        "https://gemini.google.com/": "Gemini (Google 検索連動AI)",
        "https://excelapi.org/": "ExcelAPI (外部データ連携)",
        "https://notebooklm.google.com/": "NotebookLM (資料マイニング)",
        "https://mermaid.live/": "Mermaid Live Editor (図解作成)",
        "https://gamma.app/": "Gamma (AIスライド自動生成)",
        "https://manus.im/": "Manus (次世代AIエージェント)",
        "https://studio.firebase.google.com/": "Firebase Studio (開発)",
        "https://console.firebase.google.com/": "Firebase Console (バックエンド管理)",
        "https://mixboard.google.com/": "Mixboard (クリエイティブツール)",
        "https://opal.google/": "Opal (新世代ツール)",
        "https://stitch.withgoogle.com/": "Stitch (開発支援)",
    }

    # Find the Bookmark Bar folder
    bookmark_bar_header = soup.find('h3', personal_toolbar_folder="true")
    is_in_bookmark_bar = False
    
    # We need to preserve the structure. BeautifulSoup's string representation 
    # of a parsed Netscape file might differ from the original's specific quirks.
    # We will iterate through all <a> tags and apply rules.

    for a in soup.find_all('a'):
        url = a.get('href', '')
        current_name = a.string or ""
        
        # Check if this link is inside the Bookmark Bar
        # (Technically we should check if its parent DL is under the header)
        parent_h3 = a.find_previous('h3')
        is_in_bar = parent_h3 and parent_h3.get('personal_toolbar_folder') == "true"

        # Rule 1: Bookmark Bar Cleanup
        if is_in_bar:
            if not current_name.strip():
                # Keep empty names as empty
                pass
            else:
                # Rename if it has a name
                for pattern, new_name in rename_map.items():
                    if url.startswith(pattern):
                        a.string = new_name
                        break
        else:
            # Rule 2: General Organization for items outside the bar
            for pattern, new_name in rename_map.items():
                if url.startswith(pattern):
                    a.string = new_name
                    break
            
            # If no specific rename but it's a known educational link
            if "osaka-kyoiku.ac.jp" in url:
                if "moodle" in url:
                    a.string = f"OKU Moodle {current_name if current_name else ''}"
                elif "live campus" in url.lower():
                    a.string = "Live Campus (教務システム)"
            
            # Generic cleanup: add context if name is too short
            if current_name == "sd":
                a.string = "Chrome New Tab"
            elif current_name == "字数":
                a.string = "字数カウントツール"

    # Write back
    # Note: BeautifulSoup's prettify() might break some bookmark importers 
    # that expect specific Netscape format. We'll try to keep it simple.
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    input_path = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\bookmarks_2026_04_27.html"
    output_path = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\[整理済み]bookmarks_2026_04_27.html"
    process_bookmarks(input_path, output_path)
    print(f"Processed: {output_path}")
