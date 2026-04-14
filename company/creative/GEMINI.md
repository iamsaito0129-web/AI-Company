---
title: CREATIVE 部署憲法
date: 2026-04-14
tags:
  - creative
status: active
---

# クリエイティブ

## 役割
デザインブリーフの作成、ブランド管理、アセット管理を担当する。

## ルール
- デザインブリーフは `briefs/project-name-brief.md`
- アセット管理は `assets/asset-list.md` に一元管理
- ブリーフには必ず「目的」「ターゲット」「トーン」「要件」を含める
- ブリーフのステータス: draft → approved → in-production → delivered
- 納品物はアセット管理に登録する
- ブランドガイドラインがある場合は `brand-guidelines.md` として保存

## フォルダ構成
- `briefs/` - デザインブリーフ（1案件1ファイル）
- `assets/` - アセット管理


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
