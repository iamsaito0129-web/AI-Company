# AI-Company (一人社長のAIチーム - Antigravity)

## 概要
このリポジトリは、Google Antigravity の「マルチエージェント・オーケストレーション」を活用した、自律型AIチームの運用基盤です。
秘書（Secretary）がオーナーの窓口となり、CEOが意思決定を行って専門部署（PM、リサーチ、開発、経理等）へ作業を割り振る、組織規模のAI運用を実現します。

## ディレクトリ階層と役割

```
AI-company/
├── .agent/                     # Antigravity用の技術定義コア
│   ├── skills/                 # 各部署・エージェントのスキル定義 (Custom Skills)
│   └── workflows/              # 定型業務の自動化定義
├── .company/                   # 【最新】実働データ・管理ディレクトリ（全14部署）
│   ├── GEMINI.md               # 組織のマスター設定・プロフィール・組織図
│   ├── hr/agents/              # AIエージェントの人格・権限定義（移動済み）
│   ├── creative/assets/        # ブランドアセット・ロゴ（移動済み）
│   ├── sac/                    # SAC部：校務・教育支援
│   ├── lifestyle/              # ライフスタイル部：生活・資産管理
│   └── career/                 # キャリア部：将来設計
├── projects/                   # 実装プロジェクト（ソースコード・実行環境）
│   ├── puzzle-solver/          # 3Dパズル解決アルゴリズム
│   ├── lifestyle-app/          # 生活管理ツール
│   └── insta-analyzer/         # Instagram分析ツール
├── _archive/                   # 不要ファイルの退避先
└── README.md                   # このファイル
```

## 各コンポーネントの進捗状況

### 1. .company/ (実働データ) - 【完了】
- **組織再編**: SAC（校務）、Lifestyle（生活）、Career（経歴）の3部署を統合し、全14部署体制へ拡張。
- **配置最適化**: ルートにあった `agents/` を `hr/agents/` へ、`assets/` を `creative/assets/` へ移動し、管理を一本化。
- **GEMINI.md**: 2026-04-12時点の最新ステータスに更新完了。

### 2. .agent/ (技術定義) - 【運用中】
- CEO、秘書、リサーチャーの3つのコアスキルが定義されており、Antigravity上で自律的に動作可能です。

### 3. projects/ (実装) - 【拡大中】
- 単体で動いていたプロジェクトを `projects/` 下に集約。各部署のドキュメントからこれらを参照する構造を構築。

## 今後のタスク
- [x] ルートディレクトリの整理とプロジェクトの移動
- [x] `.company/GEMINI.md` の全14部署対応
- [ ] 各部署の `_template.md` に基づいた詳細ドキュメントの拡充
- [ ] 2026年度（令和8年度）新学期データのSAC部への流し込み

---
*Last Update: 2026-04-12 | AI-Company Secretary Office*
