---
description: 朝の同期会を行い、全エージェントのタスク状況を確認して今日の優先順位を決定するワークフロー。
---

// turbo-all
1. 文脈の復元（Context Restoration）
   - `.company/secretary/logs/` 内の最新の `sync.md` を読み込み、前回のセッションの終了ステータス、未完了事項、感情的な気付きを復元する。
   - `google-calendar_get-current-time` で現在の日時を正確に把握する。

2. 多角的な情報同期（Multi-Source Gathering）
   - **Personal**: Google Calendar（本人、家族、祝日、誕生日）、Notion（本日分・未完了タスク）。
   - **Business/HR**: `hr/members/` 内の誕生日フラグや `hr/rms/RMS.md` の確認。
   - **SAC (Consulting)**: `sac/planning/` の予定を確認。授業がある場合、`sac/subjects/` の該当単元に資産（教材等）があるかチェックする。

3. 一日の戦略策定（Strategic Planning）
   - 取得した全情報を統合し、今日の「最優先ミッション」を定義。
   - `.company/secretary/todos/YYYY-MM-DD.md` を更新または生成。
   - CEO, Secretary, Researcher, SAC Consultant のそれぞれの今日のミッションを定義。

4. モーニング・ブリーフィング（Morning Briefing）
   - Artifacts を使用し、以下の構成で今日の計を可視化する。
     - **⚡ 今日の勝負所**: 1つに絞った最優先ミッション。
     - **📅 スケジュール & タスク**: タイムライン形式の予定。
     - **🎓 SAC コンサル**: 今日の授業準備状況とアドバイス。
     - **💖 家族・人間関係**: 家族の予定、メンバーの誕生日、RMS追跡候補。
   - 文末に、復元された「昨日の続き」を踏まえたAIからの最初の一声を添える。
