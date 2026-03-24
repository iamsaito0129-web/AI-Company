---
title: "モバイル・エージェント・アクセス構成"
date: "2026-03-23"
tags: ["mobile", "remote", "vscode", "cloudflare"]
---

# モバイル・エージェント・アクセス構成案

## 概略
AIエージェント（Antigravity）をスマートフォンや外出先から操作するためのリモートアクセス基盤。

## 採用方式
- **方式**: VS Code Tunnels (案C)
- **認証**: GitHub アカウントによる OAuth
- **特徴**: 
    - 完全無料。
    - 独自ドメイン不要。
    - SSL証明書管理不要。
    - ブラウザ (`vscode.dev`) からのエージェント操作環境へのアクセス。

## 設定履歴
- **2026-03-24**: 
    - `cloudflared` (Cloudflare Tunnel) のインストールを試行したが、独自ドメイン所有の要件により断念。
    - VS Code Tunnels への移行を決定。
    - UIプロトタイプ (`index.html`) の作成完了（グラスモーフィズム・デザイン）。

## 次のステップ
1. PCにて `code tunnel` を実行し、GitHub認証を完了させる。
2. 発行されたURLをモバイルブラウザで確認。
3. エージェントの制御APIを公開し、作成済みの [index.html](file:///c:/Users/iamsa/%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%BC/%E7%A7%81%E7%94%A8%28PC%29/AI-company/.company/engineering/mobile-agent-ui/index.html) と連携させる。
