---
title: "2026 03 21 organize puzzle files"
date: 2026-03-21
tags:
  - decision
  - ceo
status: resolved
obsidian-skills: optimized
---

---
date: "2026-03-21"
decision: "パズル関連ファイルの整理とプロジェクト管理下への移行"
departments: ["pm", "engineering"]
status: decided
---

# 意思決定: パズル関連ファイルの整理

## 背景
ルートディレクトリにパズル解決用のスクリプト（puzzle_solver*.py）および出力結果（3D_Route_Puzzle_Solution.html）が複数存在しており、管理が煩雑になっていた。
ユーザーよりこれらファイルの整理依頼があった。

## 判断内容
これらのファイルを独立したプロジェクト「パズル解決プロジェクト」として集約し、AI-Companyの管理体制下（PM/開発部署）に置くことを決定した。

## 振り分け先
| 部署 | 指示内容 |
|------|---------|
| 秘書室 | ファイル移動作業の実行およびクリーンアップ。 |
| PM | `pm/projects/puzzle-solving.md` の作成と進捗管理の開始。 |
| 開発 | `engineering/docs/puzzle-solver-logic.md` の作成とアルゴリズムの記録。 |

## 理由
- ルートディレクトリの整理整頓（美学要件）
- 今後のパズル解決アルゴリズムの再利用性を高めるためのドキュメント化
- プロジェクトとしてのメタデータ管理の必要性

## フォローアップ
- [x] フォルダ `パズル解決プロジェクト` の作成
- [x] 各種スクリプトの移動
- [x] __pycache__ の削除
- [ ] PMプロジェクト登録
- [ ] 開発技術ドキュメント作成
