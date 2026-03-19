# AI-Company Governance Rules

## 1. 組織理念
Antigravityのマルチエージェント・オーケストレーションを最大限に活用し、自律的に連携するAIチームとして機能する。

## 2. 組織構成
- **01_KNOWLEDGE/**: 全エージェントの共通前提知識、ルール、ユーザープロフィール。
- **02_WORKSPACE/**: 実働データ。`inbox/` (入力), `todos/` (管理), `projects/` (進行)。
- **03_TEMPLATES/**: 各種成果物の標準フォーマット。
- **04_OUTPUTS/**: 最終成果物、HQダッシュボード、リサーチレポート。
- **agents/**: 各AIエージェントの役割（ROLE.md）を定義。
- **.agent/**: 技術的なスキルとワークフローの定義。

## 3. 運営ルール
- **秘書が窓口**: ユーザーとの対話は主に Secretary が担当し、情報を `02_WORKSPACE/inbox/` に整理する。
- **CEOの指揮**: 複雑なタスクは CEO が `02_WORKSPACE/projects/` に分解・指示を出す。
- **情報の集約**: データはエージェントフォルダではなく、共通の `02_WORKSPACE/` に集約する。
- **アーティファクト中心**: 決定事項は必ず Artifacts または Markdown ファイルとして記録する。

## 4. ファイル命名規則
- **日次TODO**: `02_WORKSPACE/todos/YYYY-MM-DD.md`
- **成果物**: `04_OUTPUTS/` 内の各プロジェクトフォルダ

## 5. 学習と進化
- ユーザーの癖、好み、習慣は `01_KNOWLEDGE/profile.md` に蓄積し、全エージェントが参照する。
