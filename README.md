# AI-Company (一人社長のAIチーム)

## 概要
このリポジトリは、Claude Code の「ディレクトリ継承メカニズム」と「プラグイン・スキル」の思想を取り入れた、自律的AIエージェントチームの基盤です。
`cc-company` および `cc-secretary` の最新テンプレートに基づき、秘書を窓口とし、CEOが適切な部署へ振り分ける組織運営を実現します。

## 組織構成
- **[Secretary/](Secretary/CLAUDE.md)**: 秘書室。全ての窓口、TODO管理、壁打ち、クイックメモ。
- **[CEO/](CEO/CLAUDE.md)**: 意思決定機関。案件の部署振り分け、リスク管理。
- **[Researcher/](Researcher/CLAUDE.md)**: リサーチ部門。市場調査、技術調査、分析。
- **[reviews/](reviews/_template.md)**: 週次・月次レビュー。

## ワークスペース
- **01_ABOUT_ME/**: 創業者のプロフィールと嗜好
- **02_PROJECTS/**: プロジェクト管理資料
- **03_TEMPLATES/**: 各部署共通の品質基準
- **04_OUTPUTS/**: 最終成果物の出力場所

## 運営ルール
1. **秘書が窓口**: 何かあればまず `Secretary` フォルダのコンテキスト（または秘書の口調）で話しかけてください。
2. **自動振り分け**: 複雑な案件は、秘書が判断し CEO が適切な部署（Researcherなど）に指示を出します。
3. **テンプレート遵守**: 新規ファイル作成時は、各フォルダにある `_template.md` を使用してください。
4. **日次管理**: 毎日のタスクは `Secretary/todos/` で管理します。

---
*Created using cc-company & cc-secretary master templates.*
