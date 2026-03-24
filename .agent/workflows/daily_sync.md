---
description: 朝の同期会を行い、全エージェントのタスク状況を確認して今日の優先順位を決定するワークフロー。
---

// turbo-all
1. 現在の状況を確認する
   - `.company/secretary/todos/` 内の今日の日次ファイルを確認。
   - `google-calendar_get-current-time` で現在の日時を正確に把握する。
   - Notion データベース（「To Do リスト」および「To Do」）から、今日と明日の予定をフィルタリングして取得する。

2. エージェントのステータス更新案を作成
   - Notion のタスクとカレンダーの予定を統合し、今日のTODOリストを更新。
   - CEO, Secretary, Researcher のそれぞれの今日のミッションを定義。

3. ダッシュボードの更新
   - `.company/GEMINI.md` の現在の状況（進捗）を更新、またはサマリーを生成。

4. ユーザーへのブリーフィング
   - Artifacts を使用して、今日の全タスク（Notion 連携分を含む）と優先順位をグラフィカルに提示する。
