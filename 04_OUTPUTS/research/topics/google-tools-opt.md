# 高度調査レポート：Google ツール群による AI-Company の構築と最適化

## 1. 調査概要
ご提示いただいた「設計草案」に基づき、Google Antigravity IDE および Gemini CLI を活用した次世代 AI 組織の構築手順と、主要な技術要素（MCP, Agent Manager）の活用方法を調査しました。

## 2. システムアーキテクチャ図（視覚化）
![Google AI Company Architecture](../../google_ai_company_architecture_1773661867506.png)

## 3. 主要ツールのセットアップ手順

### ① Google Antigravity IDE (CEO室 / 統括)
Antigravity は従来の IDE の概念を超えた「エージェント・オーケストレーター」です。
- **Mission Control (Agent Manager)**: `Cmd + E` で切り替え。複数のエージェント（CEO, Researcher 等）を並行して立ち上げ、それぞれの思考プロセス、ファイル変更、ターミナル操作を監視できます。
- **Planning Mode**: complex なタスクでは必ず「Planning mode」を選択してください。エージェントが実装前に詳細なプランとタスクリストを作成し、確実性を高めます。

### ② Gemini CLI (Secretary / 実務担当)
バックグラウンドでの定型処理や高速なファイル操作を担当させます。
- **インストール**: `npm install -g @google/gemini-cli`
- **Yolo Mode (実力行使)**: `--yolo` 構文を使用することで、AI がユーザーの承認を待たずにシェルコマンドを実行し、ファイルを直接書き換えることが可能です。自動的な議事録作成や TODO 整理に最適です。
- **Context Management**: `@ファイル名` 構文により、大量の Markdown ドキュメントを即座に AI のコンテキストとして注入できます。

### ③ MCP (Model Context Protocol) サーバーの連携
外部ツール（Notion, Google Calendar, GitHub）との接続は MCP を介して行います。
- **設定場所**: Antigravity の `Settings > Connectors > MCP`
- **活用例**: 
    - `GCal MCP`: 今日の予定を取得し、Secretary が `02_WORKSPACE/todos/` に反映。
    - `Notion MCP`: 過去のナレッジを検索し、Researcher がレポートの補足に使用。

## 4. 再現手順 (Next Action)

1.  **環境の初期化**: 
    - `npm install -g @google/gemini-cli` で CLI を導入。
    - Antigravity IDE でワークスペース（AI-company フォルダ）を開く。
2.  **エージェントスキルの最終調整**:
    - `agents/CEO/ROLE.md` 等に「あなたはAntigravityのAgent Managerを通じて...」といった具体的な動作指示を追記。
3.  **MCP サーバーの有効化**:
    - 必要な MCP サーバー（Notion 等）を Antigravity に接続。

---
## 5. 結論
ご提示いただいた設計案は、Antigravity のマルチエージェント機能と Gemini CLI の機動性を組み合わせることで、**世界で最も高度な自律型 AI 開発環境**として実現可能です。特に「並列処理」によるスピードアップは、従来の Claude Code 運用を遥かに凌駕します。
