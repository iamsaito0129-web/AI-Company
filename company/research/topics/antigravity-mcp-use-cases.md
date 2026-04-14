# Antigravity MCP 活用事例レポート

## 概要
Google DeepMindが開発したエージェント型AIコーディングアシスタント「Antigravity」における、**Model Context Protocol (MCP)** の活用方法とメリットについてまとめました。

## 🛠️ MCPとは？
MCP（Model Context Protocol）は、AIモデルが外部のデータソースやツールと安全かつ効率的に通信するためのオープンな標準プロトコルです。Antigravityは、このプロトコルを介して「エディタ外」の情報にアクセスできるようになります。

---

## 🌟 主な活用事例

### 1. 🏫 教育・学校業務への応用 (Teacher Persona)
小学校教諭という多忙な役割において、Antigravityを「超強力なデジタル秘書」に変えます。
- **校内/Drive資料の直接検索**: 
  - Google Drive MCPサーバーを介して特定の学級フォルダと連携。
  - 過去の指導案や行事予定をAntigravityが直接読み込み、文脈に基づいた新しい案の作成をサポートします。
- **成績管理・名簿分析**:
  - ローカルのSQLiteやExcelに格納されたデータを、SQL系サーバー経由で安全にクエリ。
  - 「昨年のクリスマス会での役割分担はどうだった？」といった質問に対し、当時の実データを元に正確に答えます。

### 2. 👩‍💻 システム開発・技術調査 (Engineering Persona)
コーディングのアシスタントを、開発プロセス全体のオーケストレーターに進化させます。
- **APIテストの自動化**:
  - `Postman` MCPサーバーを接続。Antigravityが既存のAPI定義を読み込み、テストケースの生成から実行までを一気通貫で行います。
- **リアルタイムDB操作**:
  - `AlloyDB` や `Cloud SQL` (PostgreSQL/MySQL) に直接アクセス。
  - スキーマ情報を理解した上で、「テーブルを1つ追加し、初期データを数件挿入して」といった指示をSQLレベルで実行します。
- **セキュリティ・脆弱性チェック**:
  - `Snyk` 等のセキュリティサーバーを連携し、実装中のコードに脆弱なライブラリが含まれていないかリアルタイムで監視。

### 3. 🤖 ワークフローの自動化
- **n8n / Linear 連携**:
  - タスク管理ツールや自動化プラットフォームと連携し、Antigravityから直接チケットの進捗を更新したり、Slackのメッセージ送信をトリガーしたりします。

### 4. 📅 Google Calendar & Notion & GitHub (主要ツール連携)
日常的に使用するツールを直接操作することで、ワークフローが劇的に効率化されます。
- **Google Calendar (Gcal)**:
  - 「来週の月曜日の授業の空き時間を教えて」「放課後の会議予定を追加して」といった操作をAntigravityが代行します。
- **Notion**:
  - Notion上のデータベース（名簿や教材リンク集）を読み込み、それに基づいた週報や案を自動生成します。
- **GitHub**:
  - ソースコードだけでなく、IssueやPull Requestの管理もAntigravityから直接行えます。

---

## 💎 導入のメリット
1. **コンテキストの劇的拡大**: AIの「視野」が、ブラウザ上のソースコードだけでなく、カレンダー、メモ、外部サービスまで広がります。
2. **アクションの実行**: 単に「コードを書く」だけでなく、カレンダーに予定を書き込んだり、Notionに記録したりといった指示がAI経由で通るようになります。
3. **セキュアな連携**: 認証情報（API Key等）はMCPサーバー側でカプセル化され、AIに直接渡さずに安全なやり取りが可能です。

---

## 📝 結論
MCPを活用することで、Antigravityは単なるコーディング支援ツールから、**「組織全体のコンテキストを理解し、実際にタスクを完結させる自律的パートナー」**へと進化します。

## ⏩ ネクストアクション
- [x] Google Calendar / Notion / GitHub のMCPサーバー用テンプレートファイルを作成。
- [ ] ユーザーに各サービスのAPI トークンの発行を依頼する。
- [ ] 開発中のプロジェクトに応じたDB連携（Postgres/SQLite）を試験的に導入する。

## 🔗 出典・参考リンク
- [Model Context Protocol 公式](https://modelcontextprotocol.io/)
- [Antigravity - MCP Connection Guide](https://antigravity.google)
- [MCP Server Ecosystem (GitHub)](https://github.com/modelcontextprotocol/servers)

---
- **ステータス**: completed
- **作成日**: 2026-03-21
- **作成者**: リサーチ部署 (Antigravity)
