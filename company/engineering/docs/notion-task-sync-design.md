---
title: "Notion Task Sync Design"
date: 1774353801.6194534
tags:
  - engineering
status: active
obsidian-skills: optimized
---

# 仕様書: Notionタスク同期システム (Prototyping)

#> [!ABSTRACT]# 概要
私用PCのローカルMarkdownファイル（`secretary/todos/*.md`）と、Notionデータベース（`cdd66da2-4d97-439e-92fb-6e11bacf4ba7`）の間で、タスク情を同期させる仕組み。

## データマッピング
| Notion プロパティ | Markdown フロントマター / コンテンツ |
| :--- | :--- |
| **名前** (Title) | TODO アイテムのテキスト |
| **状態** (Status) | チェックボックス `[ ]` / `[x]` |
| **期限** (Date) | `date` または個別タスクのインライン日付 |
| **優先度** (Select) | `priority: high / normal / low` |
| **タグ** (Multi-select) | `type: daily` などのメタデータ |

## 同期ロジック（案）
1.  **Pull (Notion -> Local)**:
    -   Notionから「未完了」かつ「期限が今日〜1週間以内」のタスクを取得。
    -   ローカルの `todos/YYYY-MM-DD.md` の `## 通常` セクションに追記。
2.  **Push (Local -> Notion)**:
    -   ローカルで `[x]` になったタスクをNotion側でも `Done` に更新。
    -   新規に追加された `[ ]` タスクをNotionにレコード作成。

## 実装環境
- **言語**: Python (私用PCローカル)
- **ライブラリ**: `notion-client`
- **実行タイミング**: `antigravity` セッション同期ワークフローの一部として。

## リスク・課題
- 同期時の競合（コンフリクト）解決ルールの策定。
- すでに完了したタスクの二重登録防止。
