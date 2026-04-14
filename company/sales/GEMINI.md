---
title: SALES 部署憲法
date: 2026-04-14
tags:
  - sales
status: active
---

# 営業

## 役割
クライアント管理、提案書作成、案件パイプラインを管理する。

## ルール
- クライアントファイルは `clients/client-name.md`
- 提案書は `proposals/YYYY-MM-DD-proposal-title.md`
- クライアントのステータス: prospect → active → inactive
- 提案書のステータス: draft → sent → accepted → rejected
- コミュニケーション履歴はクライアントファイルに日付付きで追記
- 受注時はPMにプロジェクト作成を依頼、経理に請求書作成を連携

## フォルダ構成
- `clients/` - クライアント情報（1クライアント1ファイル）
- `proposals/` - 提案書（1提案1ファイル）


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
