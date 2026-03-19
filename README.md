# AI-Company (一人社長のAIチーム - Antigravity)

## 概要
このリポジトリは、Google Antigravity の「マルチエージェント・オーケストレーション」を活用し、自律的に連携するAIチームの基盤です。
秘書（Secretary）が窓口となり、CEOが意思決定を行って各部署（Researcher等）へ作業を割り振る組織運営を実現します。

## ディレクトリ階層と役割

AI-company/
├── .agent/                     # Antigravity用の技術定義コア
│   ├── skills/                 # 各部署・エージェントのスキル定義 (Custom Skills)
│   │   ├── ceo/                # `ceo` スキル: 組織構築・指示振り分け
│   │   ├── researcher/         # `researcher` スキル: 調査・分析
│   │   └── secretary/          # `secretary` スキル: 秘書業務・TODO管理
│   └── workflows/              # 定型業務の自動化定義
│       ├── daily_sync.md       # 朝の同期会ワークフロー
│       ├── deep_research.md    # 高度な調査ワークフロー
│       └── investigate.md      # 調査支援
├── .company/                   # 【最新】実働データ・管理ディレクトリ
│   ├── GEMINI.md               # 組織のマスター設定・プロフィール・案内図 (【要修正】変数未置換あり)
│   ├── ceo/                    # CEO部署のデータ
│   │   ├── GEMINI.md           # CEO固有設定 (【白紙】)
│   │   └── decisions/          # 意思決定ログ
│   │       └── _template.md    # テンプレート (【白紙】)
│   ├── secretary/              # 秘書室のデータ
│   │   ├── idea_notes/         # アイデアの欠片
│   │   │   └── _template.md    # テンプレート (【白紙】)
│   │   ├── inbox/              # 未整理情報の受け皿
│   │   │   └── _template.md    # テンプレート (【白紙】)
│   │   ├── projects/           # 進行中のプロジェクト管理
│   │   ├── reviews/            # 直近の振り返り (【白紙】template)
│   │   └── todos/              # 日次のTODO管理
│   │       └── _template.md    # テンプレート (【白紙】)
│   └── reviews/                # 組織全体の週次・月次レビュー (【白紙】template)
├── agents/                     # エージェントの人格・権限定義 (Prompt Engineering)
│   ├── CEO/
│   │   └── ROLE.md             # CEOの行動指針 (【要修正】旧パス 02_WORKSPACE 参照)
│   ├── Researcher/
│   │   └── ROLE.md             # リサーチャーの行動指針 (【要修正】旧パス 04_OUTPUTS 参照)
│   └── Secretary/
│       └── ROLE.md             # 秘書の行動指針 (【要修正】旧パス 01_KNOWLEDGE 参照)
├── 旧型：01_KNOWLEDGE/          # 古いナレッジベース (アーカイブ扱い)
├── 旧型：03_TEMPLATES/          # 古いテンプレート (アーカイブ扱い)
├── 旧型：04_OUTPUTS/            # 古い成果物 (アーカイブ扱い)
├── _archive/                   # 不要ファイルの退避先
├── .gitignore                  # 除外設定
└── README.md                   # このファイル (全体概要)


## 各ファイルの役割・状態詳細

### 1. .agent/ (技術定義)
Antigravityのスキルやワークフローを定義しています。エージェントが「何ができるか」を司ります。

### 2. .company/ (実働データ)
現在の組織運営におけるリアルタイムデータが格納されます。
- **GEMINI.md**: 全体の中心となるドキュメント。ただし、`{{ORG_CHART}}` などの変数が残っており、**【要修正】** です。
- **reviews/****: 中身の `_template.md` が **【白紙】** です。
- **_template.md**: 各フォルダ内のテンプレートが **【白紙】** 状態なものが多く、今後定義が必要です。

### 3. agents/ (役割定義)
各エージェントの「性格」や「権限」を定義します。
- **ROLE.md**: **【要修正】**。以前のディレクトリ構成（`01_KNOWLEDGE`, `02_WORKSPACE` 等）を参照しており、現在の `.company/` を使った構成とパスが一致していません。

### 4. 旧型：* シリーズ
以前の `cc-company` / `Claude Code` 時代の構成です。
- **【要修正】**: 現在のマルチエージェント構成（`.company`）に完全移行できていないため、必要に応じてデータを移行し、これらは削除または完全アーカイブ化する必要があります。

---
## 【要修正】リスト
- [x] 全体の typo: `reviwes` → `reviews` (修正済み)
- [ ] `.company/GEMINI.md`: 変数（`{{...}}`）の置換と最新化
- [ ] `agents/*/ROLE.md`: パス指定を現在の `.company/` 基準に更新
- [ ] `旧型：...` から `.company/` への完全移行

## 【白紙】リスト
- `.company/ceo/GEMINI.md`
- `.company/ceo/decisions/_template.md`
- `.company/reviews/_template.md`
- `.company/secretary/idea_notes/_template.md`
- `.company/secretary/inbox/_template.md`
- `.company/secretary/reviews/_template.md`
- `.company/secretary/todos/_template.md`

---
*Created using Antigravity AI-Company Architecture.*

