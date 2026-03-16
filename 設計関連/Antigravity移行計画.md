# AI-Company 2.0 移行計・Antigravity 最適化提案

## 1. 概要
本文書は、従来の ClaudeCode 向け構成であった `AI-company` を、Google Antigravity（Gemini）の機能を最大限に活用した次世代型 AI 組織へとアップグレードするための計画書です。

## 2. Antigravity 移行によるメリット
- **高度な視覚化**: Artifacts 機能を活用し、タスクや進捗を美しい UI で即座に確認可能。
- **ブラウザ連携**: Researcher エージェントが自律的にブラウザを操作し、動画やスクリーンショットを含むリサーチレポートを作成。
- **シームレスな自動化**: スラッシュコマンド（workflows）により、日次同期やプロジェクト開始を自動化。

## 3. 具体的な変更内容

### ① 「AI-Company HQ」ダッシュボード
エージェントの状態や TODO を一元管理する Web GUI を作成します。
- **配置先**: `04_OUTPUTS/HQ/index.html`
- **デザイン**: ユーザーの好みに合わせ、グラスモーフィズムを採用したプレミアムなデザイン。

### ② ワークフロー (Workflows) の導入
`.agent/workflows/` に以下のコマンドを追加し、操作を簡略化します。
- `/daily_sync`: 全エージェントの状況確認と指示出し。
- `/investigate`: ブラウザを使用した高度な調査。
- `/deploy_hq`: ダッシュボードの更新。

### ③ スキルの拡張
既存の `skills`（CEO, Secretary, Researcher）を Antigravity の `tool_calling` や `browser` に最適化させます。

## 4. 進行状況（2026-03-16）
- [x] Antigravity 最適化提案の作成
- [ ] AI-Company HQ (v1) のプロトタイプ作成
- [ ] ワークフローの定義と実装
- [ ] 各エージェントスキルの書き換え
