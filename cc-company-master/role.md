# cc-company ファイル構成と各ファイルの役割

このフォルダーは、Claude Code で仮想会社組織を構築・運営するためのプラグイン `cc-company` のソースコード一式です。

## ファイル構造

```
cc-company-master/
├── .claude-plugin/             # プラグインのメタデータ
│   └── marketplace.json        # マーケットプレイス登録用のカタログ情報
├── plugins/
│   └── company/                # プラグイン本体
│       ├── .claude-plugin/
│       │   └── plugin.json     # プラグインのマニフェスト（名前、バージョン、スキル定義）
│       └── skills/
│           └── company/        # スキル（AIの振る舞い）の定義
│               ├── SKILL.md    # コアロジック、オンボーディング、運営モードのワークフロー
│               └── references/ # 組織構築に使用するテンプレート群
│                   ├── departments.md         # 各部署のフォルダ構造と CLAUDE.md のテンプレート
│                   └── claude-md-template.md  # ルート CLAUDE.md のテンプレート
├── README.md                   # プラグインの概要、インストール方法、使い方
├── image.png                   # 組織構成のコンセプト図
└── LICENSE                     # MIT ライセンス
```

## 各ファイルの役割

### `plugins/company/skills/company/SKILL.md`
このプラグインの心臓部です。
- **オンボーディング**: 初回の事業ヒアリングから組織図の提案、フォルダ生成までの手順が記述されています。
- **運営モード**: 秘書が窓口となり、CEOが部署へ仕事を振り分けるためのロジックと口調ルールが定義されています。

### `references/departments.md`
各部署（秘書室、CEO、PM、開発など）がどのようなフォルダを持ち、どのような `CLAUDE.md`（ルール）で動くべきかのテンプレートが定義されています。

### `references/claude-md-template.md`
組織のルートディレクトリに生成される `CLAUDE.md` の雛形です。組織全体のガバナンスルールが記述されます。

### `.claude-plugin/`
Claude Code がこのフォルダを「プラグイン」として認識し、インストール可能にするための設定ファイル群です。
