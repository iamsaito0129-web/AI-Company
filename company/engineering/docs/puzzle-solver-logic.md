---
title: "Puzzle Solver Logic"
date: 1774058607.8822532
tags:
  - engineering
status: active
obsidian-skills: optimized
---

---
created: "2026-03-21"
topic: "3Dルートパズル・ソルバーの設計"
type: technical-doc
tags: ["algorithm", "dfs", "3d-modeling"]
---

# 3Dルートパズル・ソルバーのロジック

#> [!ABSTRACT]# 概要
5x5x10の直方体表面を移動するパズルを解決するための技術ドキュメント。
面をID化し、隣接関係をグラフ構造として定義した上で、制約付きの経路探索を行う。

## 設計・方針

### 1. 座標と面のモデリング
- 各面は `(x, y, z, face_index)` の4つ組で定義。
- `face_index` は 0〜5（+X, -X, +Y, -Y, +Z, -Z）。
- 表面に存在する面のみを抽出し、一意の `ID` を割り振る。

### 2. 隣接関係（Adjacency）
- 同じ平面上の隣接面だけでなく、角（エッジ）を曲がった先の面も考慮。
- 直進性が重視されるパズルのため、進入方向と退出方向をペアで管理する。

### 3. 最適化探索（Segments DFS）
- 単純な1ステップずつのDFSでは探索空間が広すぎるため、ターゲット（イエロー面）間の「直進セグメント」を事前に抽出。
- ターゲットを節点とするグラフを構築し、ビットマスクを用いて全ターゲット通過を確認する。

## 詳細

### ビットマスクによる状態管理
- `YELLOW_LIST` の各ターゲットに1ビットを割り当て、`curr_mask` で通過状況を管理。
- `ALL_MASK` (全ビット 1) になった時点でゴール判定を行う。

### 特定された解決ルート
- 最終的な解決には「隠された16番目のターゲット(ID: 241)」の特定が必要であった。
- `puzzle_solver_final.py` にてこの制約を含めた完全な解を算出している。

## 参考
- [[../pm/projects/puzzle-solving|パズル解決プロジェクト]]
- [puzzle_solver_final.py](../../パズル解決プロジェクト/puzzle_solver_final.py)
