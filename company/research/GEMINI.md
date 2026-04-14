---
title: RESEARCH 部署憲法
date: 2026-04-14
tags:
  - research
status: active
---

# リサーチ

## 役割
市場調査、競合分析、技術調査を行い、調査結果をまとめる。

## ルール
- 調査ファイルは `topics/topic-name.md`
- ステータス: planning → in-progress → completed
- 情報源は必ずURLまたは出典を記載
- 調査結果には必ず「結論」と「ネクストアクション」を含める
- 調査完了時は秘書に報告し、関連部署への共有を提案

## フォルダ構成
- `topics/` - 調査トピック（1トピック1ファイル）


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
