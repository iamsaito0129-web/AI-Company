---
name: neta-trend-daily
description: オーナーの活動履歴と「AI・フロント・教育」の3領域を統合した、パーソナライズ・トレンドリサーチ。
trigger: /neta-trend-daily
---

# 🚀 ワークフロー: パーソナライズ・トレンド収集 (Antigravity 用)

## 🎯 目的
オーナー（彩人さん）の現在の活動文脈（TODOやログ）を理解した上で、「AI」「フロントエンド開発」「教育 (SAC)」の3領域から、今日のアクションに繋がる有益なトレンド情報を収集・解析する。

## 🛠️ 実行手順

### 0. ユーザーコンテキストの復元

`.company/secretary/` 以下の最新 `todos/` や `logs/`、および `.company/sac/GEMINI.md` を読み込み、以下の興味領域と「現在の注力事項」を理解する：
- AI（エージェント開発、日常・教務への活用事例）
- フロントエンド開発（React/Next.js/Vue, Tailwind CSS, モダンUI/UX）
- 教育（ICT活用、EdTechトレンド、文科省のAIガイドライン、SACコンサル関連）
- 組織運営（大学祭のメンバー管理、チームビルディング、経営管理手法）
- デザイン美学（Awwwards、Dribbble等のインスピレーション）

Antigravity 独自の履歴・設定ファイルを読み込み、現在の興味領域を詳細に理解する：
- **参照ファイル**: 
    - [`.company/GEMINI.md`](file:///c:/Users/iamsa/%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%BC/%E7%A7%81%E7%94%A8%28PC%29/AI-company/.company/GEMINI.md)
    - [`.company/sac/GEMINI.md`](file:///c:/Users/iamsa/%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%BC/%E7%A7%81%E7%94%A8%28PC%29/AI-company/.company/sac/GEMINI.md)
    - [`.company/secretary/logs/latest_sync.md`](file:///c:/Users/iamsa/%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%BC/%E7%A7%81%E7%94%A8%28PC%29/AI-company/.company/secretary/logs/)
- **注力事項**: 大学祭運営、メンバー管理自動化、AIエージェント、Vue/Next.js開発、EdTechトレンド。


### 1. 多角的トレンド情報の収集 (Searching)
`search_web` および `read_url_content` を駆使して、以下の特定ソースから最新情報を取得する：

- **💡 テック・デザイン**: [Vercel Blog](https://vercel.com/blog), [Awwwards](https://www.awwwards.com/), [Hacker News](https://news.ycombinator.com/) (日本語要約).
- **🎓 教育・SAC**: [ICT教育ニュース](https://ict-enews.net/), [EdTechZine](https://edtechzine.jp/), [教育新聞](https://www.kyobun.co.jp/).
- **🇯🇵 国内市場**: はてなブックマーク ITカテゴリ（AI・プログラミング・セキュリティ）。

**AI & フロントエンド（テック・デザイン）**
- https://vercel.com/blog - Next.js / フロントエンド最新動向
- https://edtechzine.jp/ - 教育IT専門メディア（学びのアップデート）
- https://ict-enews.net/ - ICT教育ニュース（学校現場の事例・ツール）
- https://www.awwwards.com/ - 世界最高峰のウェブデザイン事例
- https://b.hatena.ne.jp/hotentry/it - 国内ITトレンド

**教育・時事（SACコンサル・教員向け）**
- https://www.kyobun.co.jp/ - 教育新聞（政策・文科省動向）
- https://resemom.jp/reseed/ - ReseEd（教育業界ニュース）
- https://www.mext.go.jp/ - 文部科学省（AIガイドライン等の一次情報）

**Reddit（13サブレッド）**
- **重要**: WebFetchツールはreddit.comをブロックするため、**Bashツールでcurlコマンドを使用**すること
- 各サブレッドから `/hot.json?t=day&limit=10` で上位10件を取得
- **old.reddit.com**を使用（www.reddit.comではない）
- User-Agentヘッダーを設定: `"User-Agent: neta-trend-collector/1.0 (trend analysis tool)"`
- 各記事の**タイトル、Redditコメントページの完全URL、投票数（ups）、コメント数**を取得
- **タイトルは日本語に翻訳して出力**

取得例（Bashツールで実行）:
```bash
curl -s -H "User-Agent: neta-trend-collector/1.0 (trend analysis tool)" \
  "https://old.reddit.com/r/programming/hot.json?t=day&limit=10" | \
  jq -r '.data.children[] | "\(.data.title)|\(.data.ups)|\(.data.num_comments)|https://www.reddit.com\(.data.permalink)"'
```

データ構造:
- `data.children[].data.title`: タイトル
- `data.children[].data.ups`: 投票数
- `data.children[].data.num_comments`: コメント数
- `data.children[].data.permalink`: パス（`https://www.reddit.com` + permalink で完全URL）

セキュリティ系（2サブレッド）:
- r/netsec
- r/cybersecurity

AI系（3サブレッド）:
- r/OpenAI
- r/LocalLLaMA
- r/ClaudeCode

コア技術系（2サブレッド）:
- r/programming
- r/technology

OSS/個人開発系（4サブレッド）:
- r/opensource
- r/indiehackers
- r/webdev
- r/javascript

キャリア/実践系（2サブレッド）:
- r/cscareerquestions
- r/productivity

### 2. 分析

収集した情報を以下の観点で分析：

**興味領域マッチング（最優先）**
- 各記事を興味領域と照合し、関連度を評価
- 高関連度の記事を「注目トピック」の最上位に配置
- 特に注目すべきトピック：
  - AI関連（教務効率化、日常へのAIエージェントの組み込み）
  - フロントエンド・デザイン（Next.js等の新機能、UI/UXのインスピレーション）
  - 教育（文科省の最新指針、学校現場でのAI・ICT成功事例）
  - 組織運営（大学祭等のチーム管理、リレーションシップ・マネジメント）
  - **「彩人の視点」**: 授業（SAC）で使えるか？ 開発中のフロントエンドに応用できるか？ 大学祭運営のヒントになるか？
- **興味度判定**: ★★★（即導入案件）〜 ★（一般教養）。


**Hacker News**
- グローバルで話題の技術トレンド
- スタートアップ・プロダクト関連
- セキュリティ関連（脆弱性、攻撃手法、インシデント）
- 議論を呼んでいるトピック（ポイント数が高い）

**Reddit（13サブレッド）**
- セキュリティ系：最新の脅威、実践的な攻撃・防御手法
- AI系：OpenAI、ローカルLLM、Claude Code関連
- OSS/個人開発系：OSSプロジェクト、個人開発、Web開発
- キャリア/実践系：キャリア、生産性
- 投票数（ups）とコメント数でコミュニティの反応を評価
- 議論が活発なトピック（コメント数が多い）を優先

### 3. 出力

**まず「ネタ収集完了。」というメッセージを返してから、分析結果を Artifacts で提示し、以下のディレクトリに保存する：**
- **保存先**: [`.company/marketing/news/YYYY-MM-DD_trend.md`](file:///c:/Users/iamsa/%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E3%83%BC/%E7%A7%81%E7%94%A8%28PC%29/AI-company/.company/marketing/news/)

以下のフォーマットで出力：

```markdown
# トレンドネタ: YYYY-MM-DD


### 注目トピック

| タイトル | ブクマ数 | 興味度 | カテゴリ | メモ |
|---------|---------|--------|---------|------|
| [タイトル](元記事URL) | XXX users | ★★★/★★/★ | AI/フロント/教育/運営 | 彩人の視点（授業、開発、経営への応用） |

**興味度の定義**:
- ★★★: 興味領域に直接関連（AI×セキュリティ、OSS、個人開発、キャリアなど）
- ★★: 間接的に関連（技術トレンド全般、エンジニアリング文化）
- ★: 一般的なIT/技術ニュース

### 全エントリー

1. [タイトル](元記事URL) (XXX users) - 概要
2. ...

## Hacker News（グローバル）

### 注目トピック

| タイトル | ポイント | 興味度 | カテゴリ | メモ |
|---------|---------|--------|---------|------|
| [タイトル](HNコメントページURL) | XXXpt | ★★★/★★/★ | AI/Security/Dev等 | 発信に活用できるポイント |

### 全エントリー

1. [タイトル](HNコメントページURL) (XXXpt) - 概要
2. ...

## Reddit（13サブレッド）

### 注目トピック

| タイトル | 投票数 | コメント数 | 興味度 | カテゴリ | サブレッド | メモ |
|---------|--------|-----------|--------|---------|-----------|------|
| [タイトル](Redditコメントページ完全URL) | XXX ups | XXX | ★★★/★★/★ | Security/AI/OSS等 | r/subreddit | 発信に活用できるポイント |

### カテゴリ別エントリー

#### セキュリティ系
1. [タイトル](RedditコメントページURL) (XXX ups, XXX comments) - r/netsec - 概要
2. ...

#### AI系
1. [タイトル](RedditコメントページURL) (XXX ups, XXX comments) - r/OpenAI - 概要
2. ...

#### OSS/個人開発系
1. [タイトル](RedditコメントページURL) (XXX ups, XXX comments) - r/opensource - 概要
2. ...

#### キャリア/実践系
1. [タイトル](RedditコメントページURL) (XXX ups, XXX comments) - r/cscareerquestions - 概要
2. ...
```

## 注意事項

- **URL必携**: すべての記事に元ソースへの完全な URL リンクを含めること。
- **翻訳**: 海外ソース（Hacker News等）のタイトルは必ず日本語に翻訳して出力すること。
- **パーソナライズ**: 文脈の抽出（Step 0）を省略せず、常に「直近のログ」を反映した結果とすること。
- **すべての記事にURLリンクを必ず含める（リンクなしは不可）**
- **Hacker NewsはHNコメントページURL（`item?id=`形式）を使用**（元記事URLではなく）
- **Hacker Newsのタイトルは日本語に翻訳**
- **RedditはRedditコメントページの完全URL（`https://www.reddit.com/r/subreddit/comments/...`形式）を使用**
- **Redditのタイトルは日本語に翻訳**
- Reddit APIレート制限に注意（1分あたり60リクエスト程度）
- 投票数（ups）/コメント数が高い記事を優先
- ポイント数/ブックマーク数が高い記事は特に注目
- 出力ファイルのYYYYMMDDは実行日の日付を使用

---

*Antigravity Optimized Trends Engine v2.0*