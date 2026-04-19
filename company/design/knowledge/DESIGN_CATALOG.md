# 📂 デザイン・ナレッジ・カタログ (Design Knowledge Catalog)

デザイン部門が分析した、再利用可能なデザインパターンの集積です。各プロジェクトの `DESIGN.md` 作成時のベースとして活用してください。

---

## 💎 登録済みデザイン・スタイル

| スタイル名 | キーワード | 主な用途 | 詳細リンク |
| :--- | :--- | :--- | :--- |
| **Pastel Fan Support** | 推し活, パステル, かわいい | イベント、個人のお祝い | [DESIGN.md](./FAN_SUPPORT_DESIGN.md) |
| **Kids Hand-Drawn** | 手書き, 温かみ, 感覚遊び | 育児支援、YouTube Kids | [DESIGN.md](./KIDS_EDUCATION_DESIGN.md) |
| **Modern Tech 3D** | 3D, クリーン, 先進的 | SaaS導入、Tech系資料 | [DESIGN.md](./MODERN_TECH_DESIGN.md) |
| **Academic EdTech** | 知的, 整理, ユーモア | 教材作成、学生向けアプリ | [DESIGN.md](./ACADEMIC_EDTECH_DESIGN.md) |
| **Educational Quiz** | 黒板, 直感, ゲーム性 | 知育クイズ、授業支援 | [DESIGN.md](./EDUCATIONAL_QUIZ_DESIGN.md) |

---

## 🛠️ デザイン抽出プロトコル (How to Use)
新しくデザイン・ナレッジを追加、または既存のものを適用する際は以下の手順に従ってください。

1.  **ソース投入**: `company/design/sources/` に画像またはPDFを配置。
2.  **メタ分析**: 配置されたファイルのカラー(HSL)、フォント、エフェクト値を特定し `analysis/` に保存。
3.  **DESIGN.md 生成**: [AGENT_DOC_STANDARD.md](../guidelines/AGENT_DOC_STANDARD.md) に基づき、実装可能な設計書を作成。
4.  **カタログ更新**: 本ファイルに対象スタイルのインデックスを追加。

---
最終更新: 2026-04-19
管理者: デザイン部門
