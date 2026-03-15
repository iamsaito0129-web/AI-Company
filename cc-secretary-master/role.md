# cc-secretary ファイル構成と各ファイルの役割

このフォルダーは、個人秘書およびライフ・ワーク管理を行うためのプラグイン `cc-secretary` のソースコード一式です。

## ファイル構造

```
cc-secretary-master/
├── .claude-plugin/             # プラグインのメタデータ
│   └── marketplace.json        # マーケットプレイス登録用のカタログ情報
├── plugins/
│   └── secretary/              # プラグイン本体
│       ├── .claude-plugin/
│       │   └── plugin.json     # プラグインのマニフェスト（名前、バージョン、スキル定義）
│       └── skills/
│           └── secretary/      # スキル（AIの振る舞い）の定義
│               ├── SKILL.md    # オンボーディング、タスク管理、管理モードのワークフロー
│               └── references/ # 管理システム構築に使用するテンプレート群
│                   ├── templates.md           # todos, ideas, research 等のファイルテンプレート
│                   └── claude-md-template.md  # 個人用 CLAUDE.md のテンプレート
├── README.md                   # プラグインの概要、インストール方法、使い方
└── LICENSE                     # MIT ライセンス
```

## 各ファイルの役割

### `plugins/secretary/skills/secretary/SKILL.md`
このプラグインのコアとなるロジックです。
- **オンボーディング**: ユーザーの役割やライフスタイルをヒアリングし、カテゴリ（フォルダ）を選択させるフローが記述されています。
- **管理モード**: 「タスク追加」「今日のタスク」「メモ（inbox）」などのクイックコマンドと、週次レビュー生成のロジックが定義されています。

### `references/templates.md`
各カテゴリ（todos, research, meetings 等）で使用されるマークダウンファイルのテンプレート集です。日付や優先度などの構造が定義されています。

### `references/claude-md-template.md`
個人管理システムのルート（`.secretary/`）に生成される `CLAUDE.md` の雛形です。パーソナライズされた秘書の振る舞いやルールが記述されます。

### `.claude-plugin/`
Claude Code がこのフォルダを「プラグイン」として認識し、インストール可能にするための設定ファイル群です。
