---
title: "Antigravity Mcp Configuration Guide"
date: 1774061927.5985062
tags:
  - engineering
status: active
obsidian-skills: optimized
---

# Antigravity MCP 設定マニュアル (Configuration Guide)

## 📌 概要
Antigravity IDEにおいて、**Model Context Protocol (MCP)** を設定し、外部サーバーやツールを統合するための技術的な手順をまとめました。

---

## 📂 1. 設定ファイルの場所
MCPの設定は、通常以下のJSONファイルで行います。どちらの場所もAntigravityは自動的に認識します。

- **ユーザー共通（全プロジェクト共通）**: 
  - `%USERPROFILE%\.antigravity\mcp_config.json` (Windows)
  - `~/.antigravity/mcp_config.json` (Mac/Linux)
- **プロジェクト別**: 
  - プロジェクトルート直下の `.antigravity/mcp_config.json`

> **Note**: ファイルが存在しない場合は、本ドキュメントの「基本構成」を参考に新規作成してください。

---

## 🏗️ 2. JSON設定の基本構造
`mcp_config.json` に、利用したいサーバーの定義を記述します。

```json
{
  "mcpServers": {
    "server-unique-id": {
      "command": "実行コマンド (例: npx, python, docker)",
      "args": ["引数1", "引数2", "..."],
      "env": {
        "SECRET_TOKEN": "必要に応じて環境変数を指定",
        "DATABASE_URL": "..."
      }
    }
  }
}
```

---

## 💡 3. 具体的な設定例

### 📁 ローカルファイルシステム連携 (Filesystem)
指定したディレクトリをAntigravityが「安全に読み書き」できるようにします。
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/iamsa/YourDataPath"]
    }
  }
}
```

### 📅 Google Calendar (Gcal)
カレンダーの読み書き、イベント作成。
```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "C:/path/to/your/gcp-oauth.keys.json"
      }
    }
  }
}
```

### 📓 Notion
Notionのページやデータベースの読み書き。
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "your_ntn_token_here"
      }
    }
  }
}
```

### 🐙 GitHub
リポジトリのIssue、PR、コードの管理。
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_ghp_token_here"
      }
    }
  }
}
```

---

## 🔒 4. セキュリティとベストプラクティス
- **秘密情報の管理**: APIキーやパスワードを `mcp_config.json` にハードコードする場合は、そのファイルがGitHubなどにアップロードされないよう、絶対パスで管理するか `.gitignore` に追加してください。
- **権限管理**: `server-filesystem` を使う際、読み取り専用にしたい場合はサーバー側の引数設定で制限してください。

---

## 🚀 5. 動作確認とトラブルシューティング
1. **設定の保存**: `mcp_config.json` を保存します。
2. **再読込**: Antigravityの「エージェントセッション」を一度リスタートするか、IDEを再読み込みしてください。
3. **ツールの確認**: Antigravityに「利用可能なMCPツールの一覧を見せて」と話しかけます。設定したサーバー名（`sqlite` など）が含まれていれば成功です。
4. **ログ確認**: 動作しない場合は、IDEの **Output** パネルから「Antigravity MCP Service」のログを確認してください。構文エラーやパスの間違いが表示されます。

---
- **最終更新**: 2026-03-21
- **作成者**: 開発部署 (Engineering Dept.)
- **ステータス**: completed
