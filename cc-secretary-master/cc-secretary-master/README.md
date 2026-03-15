# cc-secretary

Claude Code 用のパーソナル秘書プラグイン。

`/secretary` を実行すると、対話的にあなたの役割・日常・ニーズをヒアリングし、Markdownベースの管理フォルダを自動生成します。

## インストール

```
/plugin marketplace add Shin-sibainu/cc-secretary
/plugin install secretary@cc-secretary
```

## できること

**初回セットアップ（オンボーディング）**
- あなたの役割や日常をヒアリング
- 管理したい領域を選択（TODO、アイデア、リサーチ、ナレッジなど）
- ロールに最適化されたフォルダ構成を自動生成

**日常の管理（管理モード）**
- タスク追加・確認
- アイデアやリサーチのクイック記録
- inbox へのメモキャプチャ
- 週次レビューの自動生成
- ダッシュボードで全体俯瞰

## 使い方の例

```
> /secretary

秘書: あなたの主な役割や職業を教えてください！
あなた: フリーランスのWebエンジニア

秘書: 典型的な1日の流れを教えてください。
あなた: 午前はコーディング、午後はクライアントMTG、夜にレビュー

秘書: どの領域を管理したいですか？
あなた: 1,2,3,7,11

秘書: 以下のフォルダ構成を作成します...（ツリー表示）
あなた: OK

→ .secretary/ フォルダが自動生成される
```

セットアップ後は `/secretary` で管理モードに入り、日本語で操作できます:

```
> /secretary
秘書: 何をしますか？
あなた: タスク追加 APIのエラーハンドリングを修正する
```

## 管理モードのコマンド

| コマンド | 動作 |
|---------|------|
| タスク追加 [内容] | 今日のTODOにタスク追加 |
| 今日のタスク | 今日のタスクを表示 |
| メモ [内容] | inboxにクイックキャプチャ |
| アイデア [タイトル] | アイデアファイルを新規作成 |
| 調査 [タイトル] | リサーチファイルを新規作成 |
| 週次レビュー | 週次レビューを自動生成 |
| ダッシュボード | 全体概要を表示 |
| 受信箱整理 | inboxの整理を支援 |
| カテゴリ追加 [名前] | 新しいカテゴリを追加 |

## 対応カテゴリ

| カテゴリ | 説明 |
|---------|------|
| todos | デイリータスク管理 |
| ideas | アイデアの記録 |
| research | リサーチ・調査 |
| knowledge | ナレッジベース |
| content-plan | コンテンツ企画（ブログ/YouTube/SNS） |
| meetings | 議事録 |
| clients | クライアント管理 |
| journal | 日記・ジャーナル |
| reading-list | 読書リスト |
| debugging | デバッグログ |
| projects | プロジェクト管理 |
| finances | 財務・経理 |
| inbox | クイックキャプチャ（常に含む） |
| reviews | 週次・月次レビュー（常に含む） |

## ロール別プリセット

役割に応じて最適なカテゴリ構成を自動提案します:

- **ソフトウェア開発者**: todos, projects, ideas, knowledge, debugging
- **コンテンツクリエイター**: todos, content-plan, ideas, research
- **学生・研究者**: todos, courses, research, knowledge, reading-list
- **フリーランス**: todos, clients, projects, ideas, research
- **デザイナー**: todos, projects, ideas, research, knowledge
- **マネージャー**: todos, meetings, projects, knowledge

## ファイル構成

```
cc-secretary/
├── .claude-plugin/
│   └── marketplace.json              # マーケットプレイスカタログ
├── plugins/
│   └── secretary/
│       ├── .claude-plugin/
│       │   └── plugin.json           # プラグインマニフェスト
│       └── skills/
│           └── secretary/
│               ├── SKILL.md          # メインスキル定義
│               └── references/
│                   ├── templates.md  # カテゴリ別テンプレート集
│                   └── claude-md-template.md
├── README.md
└── LICENSE
```

## ライセンス

MIT
