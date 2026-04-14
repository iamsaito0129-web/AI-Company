---
title: "Archive Record"
date: 1776169340.1447086
tags:
  - project
status: active
obsidian-skills: optimized
---

---
title: Archive Record
date: 2026-04-14
tags:
  - project
status: active
---

# プロジェクトアーカイブ記録: Instagram分析アプリ (2026-03-23)

## 📑 プロジェクト状況
- **ステータス:** 一時停止 (保留)
- **中断理由:** Meta (Facebook) 開発者アカウントのセットアップ（プロアカウント連携等）の手間が現状では大きいため。
- **最終更新日:** 2026-03-23

## 🛠️ ここまでの成果物 (資産)
将来プロジェクトを再開する際、以下のファイルがそのまま利用可能です。

1. **データ取得エンジン (`backend/analyzer.py`):**
   - Instagram Graph API を使用して、指定したプロアカウントの「投稿本文」「画像」「エンゲージメント（いいね・コメント）」を自動取得・保存する Python スクリプト。
2. **セットアップガイド (`README_API_SETUP.md`):**
   - Meta for Developers でのアプリ作成、必要な権限（`instagram_basic`等）、アクセストークンの取得手順をまとめた日本語マニュアル。
3. **開発ロードマップ (`.company/engineering/docs/insta-analyzer-dev-guide.md`):**
   - ReactNative + Expo を活用したスマホアプリ化、または Web アプリとしての実装案と技術スタックの選定記録。

## 🚀 再開時のステップ
1. **Facebookアカウントの準備:** 個人アカウントをビジネス/クリエイターアカウントに紐付け、Facebookページを作成。
2. **APIトークンの取得:** `README_API_SETUP.md` に従い、アクセストークンとビジネスアカウントIDを取得。
3. **`.env` の設定:** 取得した値を `backend/.env` に記述。
4. **スクリプトの実行:** `python backend/analyzer.py` でデータのローカル保存を確認。

---
**メモ:** 
現在は「小学校勤務への新生活準備」を最優先事項としてシフトします。
このフォルダ内のソースコードとドキュメントは、そのままの状態で `projects/insta-analyzer/` に保存されています。
