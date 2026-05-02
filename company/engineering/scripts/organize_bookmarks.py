import os
from bs4 import BeautifulSoup
import re

# パス設定
input_file = r'C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\bookmarks_2026_04_27.html'
output_file = r'C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\organized_bookmarks.html'

# リネームマップ (URL -> わかりやすい表示名)
rename_map = {
    # AI・業務ツール
    'https://www.notion.so/': 'Notion (オールインワン・ワークスペース)',
    'https://www.notion.so/9788f01b7a2d480393961f654b41938b?v=347690623a9d4a638f296da04432a24c': 'Notion Inbox (タスク管理)',
    'https://chatgpt.com/': 'ChatGPT (対話型AI)',
    'https://claude.ai/': 'Claude (AIアシスタント)',
    'https://www.google.com/': 'Google 検索',
    
    # 教育・大阪教育大学
    'https://moodle5.osaka-kyoiku.ac.jp/2025/': 'OKU Moodle 2025 (学習支援)',
    'https://shrike.bur.osaka-kyoiku.ac.jp/lcu-web/': 'Live Campus (教務システム)',
    'https://osaka-kyoiku.ac.jp/': '大阪教育大学 (公式サイト)',
    'https://meaqs.btree.tech/login/index.php': 'meaQs (Moodle質問ツール)',
    'https://oku-jitsui.com/': '学園祭実行委員会 (公式サイト)',
    'https://quizlet.com/class/15799583/materials': 'Quizlet (学習カード)',
    'https://counter.sleepcows.com/': 'SleepCows (文字数カウント)',
    'https://cir.nii.ac.jp/': 'CiNii Research (論文検索)',
    'https://cloudquest.skillbuilder.aws/': 'AWS Cloud Quest (学習ゲーム)',
    'https://www.coursera.org/': 'Coursera (オンライン学習)',
    
    # 言語・翻訳
    'https://www.deepl.com/ja/translator': 'DeepL (高精度翻訳)',
    'https://textgears.com/ja/correcteur-de-grammaire-online': 'Textgears (仏語文法チェッカー)',
    'https://www.translatefrench.net/': '仏英辞書 (TranslateFrench)',
    'https://ejje.weblio.jp/': 'Weblio辞書 (英和・和英)',
    'https://www.getginger.jp/': 'Ginger (英文チェッカー)',
    'https://inokazuo.wordpress.com/': '仏語入力方法 (解説)',

    # Wargaming
    'https://asia.wargaming.net/': 'Wargaming (WoTポータル)',
    'https://tanks.gg/': 'Tanks.gg (戦車性能データ)',

    # クラファン
    'https://www.makuake.com/': 'Makuake (クラファン)',
    'https://camp-fire.jp/': 'CAMPFIRE (クラファン)',
    'https://www.kickstarter.com/': 'Kickstarter (海外クラファン)',
    'https://greenfunding.jp/': 'GREENFUNDING (クラファン)',

    # その他
    'https://education.apple.com/': 'Apple Education Community',
    'https://skillshop.exceedlms.com/': 'Skillshop (Google認定資格)',
    'https://jinro-game-e0a88.web.app/': '人狼ゲーム V3',
}

def clean_name(name):
    """不要な接尾辞や空白を削除する"""
    if not name:
        return ""
    # Google 系の長い接尾辞を削除
    name = re.sub(r' - Google (?:スプレッドシート|ドキュメント|フォーム|スライド)', '', name)
    name = re.sub(r' \| プラチナマップ', '', name)
    name = re.sub(r' – 一般社団法人日本ICT支援員協会', '', name)
    name = re.sub(r' – Feel KOBE 神戸公式観光サイト', '', name)
    name = re.sub(r' \| OKU Moodle 2025', '', name)
    return name.strip()

def organize():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} が見つかりません。")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # すべてのフォルダ(H3)をクリーンアップ
    for h3 in soup.find_all('h3'):
        original_folder_name = h3.get_text()
        cleaned_folder_name = clean_name(original_folder_name)
        h3.string = cleaned_folder_name

    # すべてのリンク(A)をリネーム
    for a in soup.find_all('a'):
        url = a.get('href', '')
        current_name = a.get_text().strip()
        
        # ユーザーのルール：表示名がないものはそのまま（空のまま）にする
        if not current_name:
            continue

        # URLの部分一致でリネームを試行
        renamed = False
        for pattern, new_name in rename_map.items():
            if url.startswith(pattern):
                a.string = new_name
                renamed = True
                break
        
        # リネームマップになかったが表示名がある場合、クリーンアップ
        if not renamed:
            cleaned = clean_name(current_name)
            
            # 特定のドメインへの個別処理（マップ漏れ対策）
            if 'osaka-kyoiku.ac.jp' in url:
                if 'moodle' in url:
                    cleaned = f"{cleaned} (Moodle)"
                elif 'shrike' in url:
                    cleaned = f"{cleaned} (学内システム)"
            
            a.string = cleaned

        # 特殊なショートカット名
        if a.string == 'sd':
            a.string = 'Chrome New Tab'

    # 結果を保存
    # Chromeが認識しやすいようにDOCTYPEやMETAタグを維持しつつ出力
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

if __name__ == '__main__':
    organize()
    print(f"整理が完了しました: {output_file}")
