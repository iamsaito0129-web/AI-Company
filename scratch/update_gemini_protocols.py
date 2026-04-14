import os

optimization_protocol = """
## 🎨 Obsidian 最適化プロトコル (obsidian-skills)

`.obsidian/skills/` に格納された公式スキルセットを**すべての Obsidian 操作のマスターガイド**として常に活用してください。

### 1. 構文と構造 (obsidian-markdown)
- **リンク**: フォルダ内の接続には `[[Wikilinks]]` を使用し、外部 URL には標準 Markdown リンクを使用する。
- **リッチコンテンツ**: `> [!TYPE]` 形式のコールアウト、`![[Embed]]` 形式の埋め込みを積極的に活用し、情報の視認性を高める。
- **プロパティ**: 全てのノートに YAML フロントマッター（`title`, `date`, `tags`, `status`）を付与し、Dataview や Bases での集計を可能にする。

### 2. 動的ビューの構築 (obsidian-bases)
- **データベース管理**: 単なるリストではなく、`.base` ファイルを用いた動的なテーブル、カード、マップビューを構築する。
- **フォーミュラ活用**: `(now() - file.ctime).days` 等のフォーミュラを用いて、ノートの「鮮度」や「進捗」を自動計算して表示する。

### 3. 自動化と整理
- Obsidian のフォルダ構造、テンプレート、CSS スニペットの変更を行う際は、常にオーナーの「プレミアムな美学（Premium Aesthetics）」と各スキルの推奨事項を両立させること。
"""

def update_gemini_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root or '.obsidian' in root:
            continue
        for file in files:
            if file == 'GEMINI.md':
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'Obsidian 最適化プロトコル' in content:
                    print(f"Skipping (already exists): {path}")
                    continue
                
                # Append before the last horizontal rule or at the end
                new_content = content + "\n" + optimization_protocol
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {path}")

if __name__ == "__main__":
    # Local workspace
    update_gemini_files(r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company")
    # Note: OneDrive path might fail due to workspace restrictions in run_command, 
    # but let's try or handle it if we can.
    # Actually, I'll just do local first since run_command works there.
