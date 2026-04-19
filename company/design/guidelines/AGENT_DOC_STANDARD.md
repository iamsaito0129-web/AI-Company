---
title: "Agent-Centric DESIGN.md Standard"
date: "2026-04-19"
tags: [engineering, guidelines, ai-agent]
status: active
---

# 🤖 AIエージェントに最適化された DESIGN.md 標準ガイドライン

AIエージェント（Antigravity等）が設計意図を正確に汲み取り、人間が期待する以上の「Premium Aesthetics」を確実に再現するためのドキュメント構成標準を定義します。

---

## 💎 1. なぜ「設計書」をAIに最適化するのか？
AIエージェントは高度な推論を行いますが、文脈の欠如や曖昧な指示があると、独自の解釈で「平凡な成果物（MVP）」に逃げる傾向があります。
再現性を高めるには、設計書を**「AIへの指示書（Command）」と「評価基準（Validator）」の統合体**として機能させる必要があります。

---

## 📂 2. 推奨される構成（The Anatomy of DESIGN.md）

### 2-1. コンセプト & 魂 (Vision & Vibe)
単なる機能説明ではなく、**「何をもって最高とするか」**を記述します。
- ❌ **Bad**: 「使いやすいログイン画面を作る」
- ✅ **Good**: 「Apple製品のような静寂と、グラスモーフィズムによる奥行きを感じさせる、没入感の高いログイン体験」

### 2-2. ビジュアル・デザイン・トークン (Visual DNA)
具体的数値を記述することで、AIがCSSを書く際の「ブレ」をなくします。
- **Color Palette**: `main: hsl(220, 80%, 50%)`, `accent: linear-gradient(...)`
- **Typography**: `Inter` (Google Fonts), `weights: 400, 700`
- **Effects**: `backdrop-filter: blur(12px)`, `border-radius: 16px`

### 2-3. 実装ロジック & アーキテクチャ (System Architecture)
データ構造と、状態遷移のルールを明示します。
- **State Table**: `INITIAL` -> `LOADING` -> `SUCCESS`
- **Schema**: JSON形式でのデータモデル定義

### 2-4. エージェント用実装プロトコル (Implementation Protocol)
**「AIよ、このように実装せよ」**という具体的な手順の指示です。
1. `index.css` にデザイントークンを CSS Variable として定義せよ。
2. 画面遷移には必ず `0.3s ease-in-out` のトランジションを付与せよ。
3. すべての画像は `placeholder` を使わず、`generate_image` で生成せよ。

### 2-5. 再現性チェックリスト (Validation Checklist)
AI自身が「完了」を報告する前に自己検閲するための基準です。
- [ ] すべてのコンポーネントはレスポンシブ対応しているか？
- [ ] ホバーエフェクト（Scale, Box-shadow）が実装されているか？
- [ ] コンソールエラーはゼロか？

---

## ✍️ 3. 書法（Writing Style）のコツ

1.  **Markdownのセマンティック（意味論）活用**:
    - `#` (H1), `##` (H2) を正しく使い、情報の階層を AI に伝える。
2.  **Callouts（コールアウト）の多用**:
    - `> [!IMPORTANT]` や `> [!TIP]` を使い、AIが読み飛ばしてはいけない「勘所」を強調する。
3.  **Few-Shot（具体的例示）**:
    - 「美しいボタン」と書かずに、そのボタンの具体的な CSS/HTML コード例を 1 つ載せるだけで再現性は 3 倍に跳ね上がる。
4.  **Enums（列挙）**:
    - 状態やタイプは、必ず列挙（A | B | C）し、AI勝手な拡張を防ぐ。

---

## 🛠️ 下書きテンプレート

以下をコピーして `DESIGN.md` の作成を開始してください。

```markdown
# [プロジェクト名]：デザイン・システム & 仕様書

## 🎯 1. ビジョン
[ユーザーにどのような「Wow」を与えたいか、1文で記述]

## 🎨 2. プレミアム・ビジュアル
- **配色**: 
- **フォント**: 
- **質感**: 

## 🏗️ 3. アーキテクチャ
- **ディレクトリ構成**:
- **データモデル**:

## ⚙️ 4. 実装プロトコル (AIエージェントへの指示)
[手順 1, 2, 3...]

## ✅ 5. 完了定義 (Definition of Done)
- [ ] 
```

---
作成者: AI-Company Engineering Dept.
最終更新: 2026-04-19
