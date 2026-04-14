---
title: "Insta Analyzer Dev Guide"
date: 1774195474.3798475
tags:
  - engineering
status: active
obsidian-skills: optimized
---

# Instagram分析スマホアプリ開発プロジェクト (ReactNative + Expo)

## 🎯 目的
- Instagram Business/Creatorアカウントのデータを取得・分析するスマホアプリの構築。
- 初のスマホアプリ開発を通じた、ReactNative + Expo の習得。

## 🛠️ 技術選定: ReactNative + Expo (Managed Workflow)
- **理由:** Web開発経験があれば、JavaScript/TypeScriptでそのまま記述でき、かつシミュレーターや実機でのプレビュー（Expo Go）が極めて容易なため。

## 📊 取得要件 (Instagram Graph API)
- **対象データ:**
    - `followers_count` (フォロワー数)
    - `media_count` (投稿数)
    - `media` オブジェクト (各投稿のいいね、コメント、Reels再生数)
- **制限事項:**
    - **アカウント種類:** 個人のInstagramアカウントは不可。BusinessまたはCreatorアカウントが必要。
    - **連携:** Facebook Page との紐付けが必須。
    - **Rate Limit:** 1アカウントあたり200リクエスト/1時間。

## 🚀 開発ロードマップ (Step 1)
1.  **環境構築:**
    - `npm install -g expo-cli` (必要に応じて)
    - `npx create-expo-app InstaAnalyzer`
2.  **Meta for Developers セットアップ:**
    - Appの作成、Instagram Graph API の許可設定。
3.  **プロトタイプ作成:**
    - OAuth認証の実装 (`AuthSession` を使用)。
    - 基本情報の取得テスト。

---

## 📅 新生活・教員準備ガイド (補足)
- **【最優先】3月のうちに:** 4月からの勤務先（学校）から「初日の持ち物」が郵送または連絡されているはずです。特に「免許状の原本」などは直前に慌てないよう整理しておいてください。
- **【教員スキル】:** 「自己紹介スライド」をCanvaなどで作成しておくと、初対面の子供たちの心を掴むのに役立ちます。
