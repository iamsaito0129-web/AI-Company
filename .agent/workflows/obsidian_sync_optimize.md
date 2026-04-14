# 🚀 Obsidian 同期・最適化ワークフロー (obsidian_sync_optimize)

## 🎯 目的
直近で編集されたファイルを特定し、`.obsidian/skills/` のガイドラインに基づいて Obsidian に最適化（プロパティ付与、リンク構造化、美学適用）を行う。

## 🛠️ ステップ

1. **実行日時の取得とステータス確認**:
    - `.company/secretary/status/obsidian_optimization_status.md` を読み取り、前回の最終実行日時を確認する。

2. **対象ファイルの抽出**:
    - `git log --since="[最終実行日時]" --name-only` またはファイルシステムの更新日時を基に、前回実行以降に更新された `.md` ファイルをリストアップする。

3. **最適化の実施 (参照: .obsidian/skills/)**:
    - 各ファイルに対し、以下の処理を自律的に行う：
        - **YAML Properties**: `date`, `tags`, `status` 等の標準プロパティが欠落している場合は付与する。
        - **Structure**: 必要に応じて `[[Wikilinks]]` やコールアウトを導入し、ナレッジの接続性を高める。
        - **Aesthetics**: Obsidian内での表示が「プレミアム」になるよう調整する。

4. **ステータスの更新**:
    - 全ファイルの最適化が完了したら、`.company/secretary/status/obsidian_optimization_status.md` の「最終実行日時」を現在の時刻に更新し、実行履歴を追記する。

5. **セッション同期の呼び出し**:
    - 最後に `[[/sync_session]]` を実行し、変更を Git に刻印する。

---
※このワークフローは、定期的なメンテナンス時や、大量の資料をインポートした後に実行することを推奨する。
