---
title: デザイン部門 部署憲法
date: 2026-04-19
tags:
  - design
status: active
---

# デザイン部門 (Design Department)

## 役割
視覚的情報の構造化と、ブランドの美学の統括を担当する。
画像やPDFなどの非構造化データから、AIエージェントが理解・再現可能な「DESIGN.md」を生成し、ナレッジとして管理する。

## ルール
- 提供されたデザインソースは必ず `sources/` に保存してから分析を開始する
- 分析レポートは `analysis/` に論理的に記述する
- 確定した設計書は `knowledge/` に蓄積し、`DESIGN_CATALOG.md` を更新する
- 常に「Premium Aesthetics」を追求し、単なるMVP（最小限機能）に妥協しない
- CSSの定義には、具体的数値（HSL, px, rem）とフォント名を明記する

## フォルダ構成
- `sources/` - 分析対象のオリジナルファイル
- `analysis/` - 中間解析レポート・スタイル抽出
- `knowledge/` - 完成した DESIGN.md とカタログ
- `guidelines/` - 会社全体のデザイン基準・標準ドキュメント
- `projects/` - 進行中のデザイン特化タスク

---

## 🎨 Obsidian 最適化プロトコル (obsidian-skills)

`.obsidian/skills/` に格納された公式スキルセットを**すべての Obsidian 操作のマスターガイド**として常に活用してください。

### 1. 構文と構造 (obsidian-markdown)
- **リンク**: フォルダ内の接続には `[[Wikilinks]]` を使用し、外部 URL には標準 Markdown リンクを使用する。
- **リッチコンテンツ**: `> [!TYPE]` 形式のコールアウト、`![[Embed]]` 形式の埋め込みを積極的に活用し、情報の視認性を高める。
- **プロパティ**: 全てのノートに YAML フロントマッター（`title`, `date`, `tags`, `status`）を付与する。

### 2. 動的ビューの構築 (obsidian-bases)
- **カラーデータベース**: 各スタイルの配色データを抽出して一括管理する仕組みを構築する。

---
最終更新: 2026-04-19
ステータス: Active
