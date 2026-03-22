# Instagram API セットアップ手順書 (2026年版)

このプロジェクトを動かすには、Meta(Facebook)の開発者アカウントを介してAPIキーを取得し、`backend/.env` に反映させる必要があります。

## 1. 事前準備 (スマホ・ブラウザ)
- [ ] Instagramアカウントを「プロアカウント(ビジネス or クリエイター)」に変更。
- [ ] Facebookページを作成し、Instagramアカウントを「リンク済みアカウント」として連携。

## 2. Meta for Developers での操作
- [ ] [Meta for Developers](https://developers.facebook.com/) で新規アプリを作成(タイプ: その他/ビジネス)。
- [ ] 「グラフAPIエクスプローラ」を開く。
- [ ] 以下の権限(Permissions)を取得:
    - `instagram_basic`
    - `instagram_manage_insights`
    - `pages_show_list`
    - `pages_read_engagement`
- [ ] 「Generate Access Token」をクリックし認証。

## 3. IDの取得
- [ ] グラフAPIエクスプローラで `me/accounts?fields=instagram_business_account{id,name}` を実行し、IDをコピー。

## 4. トークンの長期化 (推奨)
- [ ] [アクセストークンデバッガー](https://developers.facebook.com/tools/debug/accesstoken/) でトークンを延長。

## 5. .env への反映
取得した以下の2つの値を `backend/.env` に貼り付けてください。

```env
INSTAGRAM_ACCESS_TOKEN=取得した長期トークン
INSTAGRAM_BUSINESS_ACCOUNT_ID=取得したビジネスアカウントID
```
