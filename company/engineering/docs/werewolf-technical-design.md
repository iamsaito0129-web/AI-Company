---
title: "Werewolf Technical Design"
date: 1773942979.1598334
tags:
  - engineering
status: active
obsidian-skills: optimized
---

# 🐺 人狼：魔導書 (Werewolf: The Grimoire) 技術仕様書

## 1. 概要
本作は Vue 3 (CDN) と Firebase Realtime Database を使用した、リアルタイム対戦型の人狼ゲームです。
「魔導書」をテーマとしたダークでプレミアムなデザイン、および複雑な特殊役職の自動解決を特徴としています。

## 2. システム構成
- **Frontend**: Vue 3 (Composition API, ESM Browser version)
- **Backend**: Firebase Realtime Database
- **Auth**: Firebase Anonymous Authentication
- **Asset**: Gemini AI 生成によるオリジナルイラスト

## 3. ディレクトリ構造
```bash
online 人狼/
├── index.html           # エントリーポイント
├── public/              # 静的アセット（ビルド済みの構成を模倣）
│   ├── images/          # 役職イラスト・背景
│   └── src/             # (Firebase用デプロイ構成)
├── src/                 # ソースコード
│   ├── App.js           # メインコンポーネント (Viewの切り替え、Modal管理)
│   ├── assets/          # スタイルシート
│   ├── components/      # UIコンポーネント
│   ├── composables/     # ビジネスロジック (Firebase同期、状態管理)
│   └── views/           # 画面単位のビュー
```

## 4. 状態管理 (`useGameState.js`)
Firebase Realtime Database のパス `rooms/${roomId}` を唯一の正解（Single Source of Truth）として同期します。

### 4-1. ルームデータ構造
```json
{
  "phase": "LOBBY | DAY | VOTE | NIGHT | GAME_SET",
  "turn_count": 1,
  "host_uid": "STRING",
  "players": {
    "uid_abc": { "name": "Name", "is_alive": true, "is_spectator": false }
  },
  "config": {
    "knightSelfGuard": false,
    "voteTie": "NO_EXEC | RANDOM",
    "seerFirstDay": "RANDOM_WHITE | FREE | NONE"
  },
  "actions": {
    "turn_1": {
      "votes": { "uid_me": "target_uid" },
      "wolf_actions": { "uid_wolf": "target_uid" },
      "seer_actions": { "uid_seer": "target_uid" },
      "suspect_actions": { "uid_villager": "target_uid" }
    }
  },
  "last_phase_result": "STRING (朝のメッセージ等)"
}
```

### 4-2. 秘匿情報 (`roles/${roomId}`)
役職、および占い師/霊能者が得た「知識」は、ルームデータとは別のパスに保存され、Firebase Rules（予定）またはクライアント側のフィルタリングによって秘匿されます。

## 5. フェーズ遷移ロジック
ホスト（GM）のクライアントが `checkAutoResolve` を実行し、全員の入力が完了した時点で `resolvePhase` を呼び出します。

1. **LOBBY**: 参加待機、役職構成設定
2. **DAY**: 話し合い（タイマー起動）
3. **VOTE**: 処刑投票（Mayoerは2票、同数時はconfigに従う）
4. **NIGHT**: 能力行使（Werewolf, Seer, Hunter, Thief, etc.）
5. **GAME_SET**: 勝敗判定、全役職開示

## 6. 特殊役職の実装状況
- **猫又 (NEKOMATA)**: 処刑時にランダム道連れ、襲撃時に人狼道連れ（実装済み）
- **妖狐 (FOX)**: 襲撃耐性、占われると死亡（実装済み）
- **パン屋 (BAKER)**: 生存時に朝のメッセージ変化（実装済み）
- **狂信者 (FANATIC)**: 人狼の正体を把握（実装済み）
- **役人 (MAYOR)**: 投票数 2票（実装済み）
- **人狼 (WEREWOLF)**: 多数決による襲撃（実装済み）

## 7. 今後の拡張予定
- [ ] 狂信者以外の「チーム狼」への人狼把握機能
- [ ] 多彩な天候（WEATHER）によるゲームへの影響（STORM以外の追加）
- [ ] 各役職固有のマイクロアニメーション演出
