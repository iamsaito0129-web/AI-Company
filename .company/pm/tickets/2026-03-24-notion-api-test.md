---
created: "2026-03-24"
project: "notion-task-sync"
assignee: "Engineering/Dev"
priority: high
status: open
---

# TICKET: Notion API 連携テストスクリプトの作成

## 内容
- Python を使用して、Notion DB (`cdd66da2-4d97-439e-92fb-6e11bacf4ba7`) からタスク一覧を取得するプロトタイプを作成する。
- 期限 (`Date`)、ステータス (`Status`)、タイトル (`Name`) のフィールドが正しく読み取れることを検証する。

## 完了条件
- [ ] Notion API キーを用いて DB に接続できる。
- [ ] 最新の 10 件のタスクを JSON/Markdown 形式でコンソール出力できる。
- [ ] エラーハンドリング（ネットワークエラー、API制限等）の基本実装。

## メモ
- 同期システムの最初のステップとなる重要な調査・実装タスク。
