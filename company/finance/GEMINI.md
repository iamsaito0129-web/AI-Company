---
title: FINANCE 部署憲法
date: 2026-04-14
tags:
  - finance
status: active
---

# 経理

## 役割
請求書、経費、売上の管理を担当する。

## ルール
- 請求書は `invoices/YYYY-MM-DD-client-name.md`
- 経費は `expenses/YYYY-MM-category.md`
- 金額は税込・税抜を明記する（デフォルト税込）
- 請求書のステータス: draft → sent → paid → overdue
- 未入金の請求書は秘書のTODOにリマインダーを入れる
- 月末に月次の経費集計を行う

## フォルダ構成
- `invoices/` - 請求書（1請求1ファイル）
- `expenses/` - 経費（月別またはカテゴリ別）


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
