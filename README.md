# AI-Company (一人社長のAIチーム - Antigravity)

## 概要
このリポジトリは、Google Antigravity の「マルチエージェント・オーケストレーション」を活用した、自律型AIチームの運用基盤です。
秘書（Secretary）がオーナーの窓口となり、CEOが意思決定を行って専門部署（PM、リサーチ、開発、経理等）へ作業を割り振る、組織規模のAI運用を実現します。

## ディレクトリ階層と役割

```
AI-company/
├── .agent/                     # Antigravity用の技術定義コア
│   ├── skills/                 # 各部署・エージェントのスキル定義 (Custom Skills)
│   │   ├── ceo/                # `ceo` スキル: 組織構築・意思決定・指示振り分け
│   │   ├── researcher/         # `researcher` スキル: 調査・分析・レポート
│   │   └── secretary/          # `secretary` スキル: 秘書業務・TODO・ナレッジ管理
│   └── workflows/              # 定型業務の自動化定義
│       ├── daily_sync.md       # 朝の同期会ワークフロー
│       ├── deep_research.md    # 高度な調査ワークフロー
│       └── investigate.md      # 調査支援
├── .company/                   # 【最新】実働データ・管理ディレクトリ
│   ├── GEMINI.md               # 組織のマスター設定・プロフィール・組織図（完成）
│   ├── ceo/                    # CEO（意思決定ログ、振り分け基準）
│   ├── secretary/              # 秘書室（TODO、アイデア、ナレッジ等 15カテゴリ）
│   ├── reviews/                # 組織全体の週次・月次レビュー
│   ├── pm/                     # PM（プロジェクト、チケット管理）
│   ├── research/               # リサーチ（調査トピック、レポート）
│   ├── marketing/              # マーケティング（コンテンツ企画、キャンペーン）
│   ├── engineering/            # 開発（技術ドキュメント、デバッグログ）
│   ├── finance/                # 経理（請求書、経費管理）
│   ├── sales/                  # 営業（クライアント管理、提案書）
│   ├── creative/               # クリエイティブ（デザインブリーフ、アセット）
│   └── hr/                     # 人事（採用管理、オンボーディング）
├── agents/                     # エージェントの人格・権限定義 (Prompt Engineering)
│   ├── CEO/                    # 【要修正】旧パス参照(02_WORKSPACE等)が残存
│   ├── Researcher/
│   └── Secretary/
├── _archive/                   # 不要ファイルの退避先（過去の設計草案など）
└── README.md                   # このファイル
```

## 各コンポーネントの進捗状況

### 1. .company/ (実働データ) - 【完了】
- **組織構築**: 基本11部署すべてのフォルダ構築とサブディレクトリの作成が完了しました。
- **GEMINI.md**: 組織マスタードキュメント。変数の置換、組織図（ASCIIアート）、部署役割、フォルダ目的のすべてを現在のフル構成に合わせて完成させました。
- **テンプレート**: 秘書室の15カテゴリ、各部署の専門カテゴリすべてに `_template.md` を配備し、内容の流し込みも完了しています。
- **GEMINI.md (部署別)**: 各部署ルートに、役割とルールを定義した部署別「憲法」を配備しました。

### 2. .agent/ (技術定義) - 【運用中】
- CEO、秘書、リサーチャーの3つのコアスキルが定義されており、Antigravity上で自律的に動作可能です。

### 3. agents/ (役割定義) - 【要修正予定】
- **ROLE.md**: 現在、人格定義内のパス指定が旧ディレクトリ構成（`01_KNOWLEDGE` 等）を参照しています。今後、新設した `.company/` 基準へのパス書き換えが必要です。

## 今後のタスク
- [x] `.company/GEMINI.md`: 変数置換と組織図の完成
- [x] `.company/` 以下の全テンプレート・全部署GEMINI.md配備
- [x] 秘書室 (secretary) の全15カテゴリ拡張
- [x] `agents/*/ROLE.md`: パス指定を `.company/` 基準に一括更新
- [x] 旧型ディレクトリからのデータ完全移行と削除

---
*Created using Antigravity AI-Company Architecture.*
