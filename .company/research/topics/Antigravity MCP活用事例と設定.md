# **Google AntigravityにおけるModel Context Protocol (MCP)の高度活用事例と最適設定手法に関する包括的研究報告**

## **序論：エージェントファースト型統合開発環境の台頭とコンテキストの壁**

ソフトウェアエンジニアリングの歴史は、抽象化と自動化の絶え間ない進化の過程であると言える。従来の統合開発環境（IDE）は、静的コード解析に基づくシンタックスハイライトや、局所的な文脈に依存するコード補完（オートコンプリート）を提供するツールに留まっていた。しかし、近年の大規模言語モデル（LLM）の飛躍的な進化に伴い、開発環境は新たなパラダイムへと移行しつつある。Googleが発表した「Google Antigravity」は、この次世代の潮流を牽引するエージェントファースト（Agent-first）型の開発プラットフォームである1。Antigravityは、単なるコードジェネレーターではなく、Gemini 3 Proをはじめとする最先端の推論モデルを中核に据え、複数のAIエージェントが自律的にタスクを計画し、実行し、検証する「ミッションコントロール」として機能するように設計されている2。

このプラットフォームにおいて特筆すべきは、マルチエージェント協調システムの導入である。例えば、あるエージェントが複数ファイルにまたがるコード生成を担う一方で、別のエージェントが組み込みのChromeブラウザインスタンスを操作してUIのテストやデバッグを並行して実行するといった高度なオーケストレーションが可能となっている3。従来のAIコーディングアシスタントが単一のプロンプトに対する一問一答形式の応答に終始していたのに対し、Antigravityは自律的なアクターとして振る舞い、人間の介入を最小限に抑えながら複雑なエンジニアリングタスクを反復的に解決していく能力を備えている2。

しかしながら、エージェントの推論能力がいかに強力であろうとも、その実効性はエージェントがアクセス可能な「情報（コンテキスト）」の質と量に完全に依存するという根本的な制約が存在する。AIエージェントが真に実用的なアプリケーションを構築するためには、ローカルに存在するソースコードのテキスト情報だけでなく、クラウド上で稼働するデータベースのスキーマ、サードパーティAPIの最新仕様、CI/CDパイプラインのビルドログなど、外部環境の動的な状態を正確に把握する必要がある1。従来、これらの情報は開発者が手動で検索し、エディタのチャットウィンドウにコピー＆ペーストすることでAIに与えられていたが、この手動プロセスは著しく非効率であり、情報の陳腐化や文脈の欠落を引き起こす原因となっていた6。

このコンテキストの壁を打ち破り、AIエージェントと広範な開発環境をシームレスに結合するための技術的ブレイクスルーが「Model Context Protocol（MCP）」である。本報告書では、AntigravityにおけるMCPのアーキテクチャ的役割を定義した上で、データベース統合、アーキテクチャ解析、自律的品質保証（QA）、クラウドコスト最適化といった多岐にわたる実践的な活用事例を詳細に分析する。さらに、システム要件の整備からローカルおよびリモートMCPサーバーの高度なカスタム設定手法、さらにはエージェントの推論プロセスを制御するためのプロンプトエンジニアリングやトラブルシューティングに至るまで、開発現場での要求を満たす包括的な設定手法を論じる。

## **Model Context Protocol (MCP) のアーキテクチャ的役割**

Model Context Protocol（MCP）は、AIアプリケーションと外部のデータソースやツールとの間を接続するための標準化されたプロトコルである。この技術は、しばしば「AIのためのUSB-Cポート」や「ユニバーサル翻訳機」という比喩で表現される1。Antigravity環境におけるMCPの導入は、エージェントの能力を局所的なファイルシステムの操作から、エンタープライズ規模の分散システム全体のオーケストレーションへと拡張する中核的なメカニズムとして機能する。

MCPのアーキテクチャは、複数のサーバーに対して同時に、かつ透過的に接続を確立する能力を持つ7。これにより、エージェントはローカルツールとリモートツールを区別することなく、単一のインターフェースを通じて広範なリソースを操作することが可能となる7。AntigravityにおけるMCPの機能は、大きく分けて「コンテキストリソースの動的提供」と「カスタムツールの安全な実行」という二つの柱によって構成されている。

第一の柱であるコンテキストリソースの動的提供は、エージェントの推論に必要な外部データをリアルタイムでエディタ環境に注入するメカニズムである6。例えば、開発者がSQLクエリを記述する際、AntigravityのエージェントはMCPを通じて本番環境またはステージング環境のNeonやSupabaseなどのデータベースに直接接続し、ライブスキーマを検査する6。これにより、AIは幻覚（ハルシネーション）に基づく架空のテーブル名やカラム名を提案することなく、実在する正確な識別子を用いたクエリを生成できる6。また、デバッグの文脈においては、NetlifyやHerokuといったプラットフォームから最新のデプロイメントログやビルドログを動的に取得し、エラーの根本原因を特定するための文脈として活用する6。

第二の柱であるカスタムツールの安全な実行は、エージェントに対して特定のアクションを委譲する機能である6。MCPサーバーは、AIが実行可能なアクション（ツール）のセットを定義し、それぞれのアクションに対する入力スキーマと権限境界を厳格に管理する6。具体例として、コードベース内に残されたTODOコメントをエージェントが自律的に検出し、「Linearにタスク発行用のIssueを作成する」といったプロジェクト管理システムとの連携が挙げられる6。さらに、新しい認証機能を実装する際に「NotionやGitHubの社内リポジトリを検索し、組織標準の認証パターンの実装例を取得する」といったナレッジベースへのクエリ実行も、エディタから離脱することなくシームレスに行われる6。

以下の表は、MCPプロトコルが提供する主要な機能カテゴリとその具体的な実装例を整理したものである。

| 機能カテゴリ | 役割とメカニズム | Antigravityにおける具体例 |
| :---- | :---- | :---- |
| **コンテキストリソースの統合** | 外部データソースからリアルタイムの情報を読み取り、推論の精度と事実的正確性を向上させる。 | Neon/Supabaseのスキーマ検査に基づくSQL生成。Netlify/Herokuからのビルドログ動的取得6。 |
| **カスタムツールの実行** | 外部システムに対して安全に定義された操作（書き込み・状態変更・検索）を自律的に実行する。 | LinearへのIssue自動作成。NotionおよびGitHubを対象としたアーキテクチャパターンの検索6。 |
| **透過的マルチサーバー接続** | ローカルおよびリモートに存在する複数のMCPサーバーへ同時接続し、境界を意識させない統合環境を提供する。 | BigQuery（リモート）とASTパーサー（ローカル）を組み合わせたデータ駆動型のコード解析1。 |

このように、MCPはAntigravityにおけるAIエージェントの「感覚器官」および「操作用の手足」として機能し、抽象的な指示を具体的なシステム上のアクションへと変換する基盤となっているのである。

## **インフラストラクチャおよびデータベースの自律的オーケストレーション**

最新のエンタープライズアプリケーションにおいて、データインフラストラクチャは極めて複雑化しており、開発者がそれらの構成や状態を完全に記憶・把握することは事実上不可能である。この課題に対し、Google CloudはAntigravity向けに「MCP Toolbox for Databases」を公開し、データアナリティクスサービスとAIエージェントの直接的な統合を実現した1。このツールボックスの導入により、複雑な接続設定ファイルを手動で記述する従来の苦労は排除され、UI駆動の直感的なプロセスを通じてセキュアなデータベース接続が確立される1。

### **サポートされるデータインフラとツール群**

MCP Storeには、AlloyDB for PostgreSQL、BigQuery、Spanner、Cloud SQL (MySQL, PostgreSQL, SQL Server)、Dataplex、Lookerなど、Google Cloudのエコシステムを網羅する多様なサーバーがネイティブ統合されている1。これにより、エージェントは抽象的な推論レイヤーから、データ認識を伴う具体的なアクションレイヤーへと進化を遂げた1。

エージェントが自律的に呼び出すことが可能なデータベース向けの具体的なツール群は、データベース操作、リソース管理、およびオブザーバビリティ（可観測性）の各領域にまたがっている。以下の表は、MCP Toolboxが提供する代表的なツール群の詳細を示している。

| ツールカテゴリ | ツール名 | 機能詳細と利用シナリオ |
| :---- | :---- | :---- |
| **データベース操作** | list\_tables | 対象データベース内の全テーブルリストおよび対応するディスクリプションを抽出する9。スキーマ理解の初期段階で活用。 |
|  | execute\_sql | 任意のSQLステートメントを実行する9。データのサンプリングや、DDLによるスキーマ変更を伴う操作に利用。 |
|  | get\_query\_plan | Cloud SQL等のインスタンスにおいて、単一ステートメントのクエリ実行計画（EXPLAIN結果）を取得する9。 |
|  | list\_tables\_missing\_unique\_indexes | プライマリーキーやユニークインデックスが欠落している非効率なテーブルをシステム的に検出する9。 |
| **リソース管理** | create\_database | クラウドインスタンス内に新規データベースを自律的に作成する9。 |
|  | list\_instances | 特定のGoogle Cloudプロジェクト内に存在するデータベースインスタンスの全容を一覧表示する9。 |
| **オブザーバビリティ** | get\_system\_metrics | 対象インスタンスのCPU、メモリ、ディスクI/O等のシステムレベルのパフォーマンス指標を取得する9。 |
|  | get\_query\_metrics | 実行時間の長いクエリやロックの待機時間など、クエリ関連のメトリクスを動的に収集する9。 |

### **データインフラ最適化のパラダイムシフト**

これらのツールがAIエージェントに提供されることで、開発ワークフローは事後対応型から事前予測型へと劇的に変化する。例えば、開発者がO/Rマッパー（ORM）を用いて複雑なデータ取得ロジックを記述したとする。従来であれば、このコードが本番環境でパフォーマンス劣化（例えばN+1問題やフルテーブルスキャン）を引き起こすまで問題が顕在化しないケースが多い。しかし、Antigravity環境下では、エージェントが自律的にget\_query\_metricsを監視し、非効率な兆候を検知した段階で即座にget\_query\_planを発行するシナリオが可能となる9。エージェントは実行計画を解析し、インデックスが不足しているテーブルを特定（list\_tables\_missing\_unique\_indexesの活用など）した上で、最適なインデックス付与のためのDDL文を提案し、承認を得てexecute\_sqlで適用する、という一連のアーキテクチャ最適化プロセスを完遂することができるのである9。

### **FinOpsにおけるビッグデータ解析と自動スクリプト生成**

データベースMCPの応用範囲は、アプリケーションのコード生成のみに留まらない。クラウドインフラストラクチャのコスト最適化（FinOps）領域においても、その威力が実証されている。クラウドエンジニアにとって、GCPの課金コンソールに表示される突発的なコストスパイクの原因を特定することは、極めて難易度の高い作業である10。SKU（Stock Keeping Unit）ごとにグループ化された標準のダッシュボードでは、「どのCloud Runサービスがコストを押し上げているのか」「そのコストはインスタンスの起動時間によるものか、リクエスト数によるものか」「Cloud Loggingの急増の原因となっている特定のリソースは何か」といった粒度の細かい問いに答えることはできない10。

通常、この問題を解決するためには、GCPの課金データをBigQueryにエクスポートし、データエンジニアが巨大で複雑なSQLの集計クエリを手動で記述し、結果を繋ぎ合わせるという多大な労力を要するプロセスが必要となる10。しかし、AntigravityとBigQuery MCPを組み合わせることで、開発者はこの煩雑なプロセスをAIエージェントに完全に委譲することができる10。開発者が「直近の課金スパイクの原因を特定するスクリプトを作成せよ」と指示すると、エージェントはBigQuery上の課金データスキーマを動的に解析し、適切なデータスライスを行うSQLを自律的に構築する10。さらに、エージェントはその結果を基にして、開発者の環境に合わせた再利用可能かつ高度に粒度化されたFinOps用Bashスクリプト（カスタムCLI）をわずか数時間で自動生成する10。これは、MCPを通じたデータベースコンテキストへの直接接続が、運用監視プロセスにおける不透明性を排除し、インサイトの抽出速度を桁違いに向上させることを明確に示している。

## **大規模アーキテクチャにおける文脈飽和の回避とコードインテリジェンス**

AIコーディングエージェントが直面する最大の技術的障害の一つが「文脈飽和（Context Saturation）」である11。モダンな大規模言語モデル（例えばGemini 3 ProやClaude 4.5）は膨大なコンテキストウィンドウを誇るが、大規模なマイクロサービス・アーキテクチャなどのコードベースにおいて、関連情報を力技で探索しようとすると急速に性能が劣化する8。

### **Grep探索の限界とASTベースのMCPサーバーの導入**

開発者が「配送フロー（shipping flow）の仕組みはどうなっているか？」といった抽象的な質問をAntigravityに投げかけた場合、標準的な動作ではエージェントはファイルシステム内を無差別にGrep（文字列検索）し、関連しそうな数十のファイルを次々と開いて内容を読み込もうとする8。このアプローチは極めて遅延が大きく、大量のノイズ（無関係なコード行）をコンテキストウィンドウに混入させるため、最終的にエージェントがコンテキストを消費し尽くし、当初の目的を忘却してしまうという事態を引き起こす8。文字列の単純なパターンマッチングは、大規模コードベースの構造的理解には全く不適格なのである8。

この深刻な問題に対するエレガントな解決策が、コードを事前にインデックス化するコードインテリジェンス専用のMCPサーバーの導入である。ある実践的な事例では、Go言語で記述された約10のマイクロサービス群に対して、コードのAST（抽象構文木：Abstract Syntax Tree）を解析し、関数呼び出しの依存関係（コールグラフ）をNeo4jのようなグラフデータベースに構築し、さらにセマンティック検索機能を付与するカスタムMCPサーバー（例：goatlas）が構築・統合された8。

この環境下では、Antigravityのエージェントは手当たり次第にファイルを読み込むのではなく、MCPサーバーが提供するfind\_callers（呼び出し元の特定）、trace\_type\_flow（型情報のデータフロー追跡）、analyze\_impact（コード変更時の影響範囲分析）といった高度に抽象化されたツールを呼び出す8。これにより、エージェントはわずか1〜2回のクリーンなツール呼び出しで、関数の依存ツリーやシステム全体のアーキテクチャ設計を瞬時かつ正確に把握することができるようになる8。結果として、コード発見のための試行錯誤が激減し、コンテキストが極めてクリーンな状態に保たれるため、エージェントは複雑なタスクの途中で状態を見失うことなく、高精度のコード生成やリファクタリングを完遂できるのである8。さらに、このMCPはファイルの編集をリアルタイムに検知してインデックスを自動更新するフック機能を備えており、セッション開始時に最新のアーキテクチャの文脈をエージェントに注入する役割も果たす8。

### **リトリーバーおよび逐次推論サーバーの活用**

コードの文脈管理をさらに強固なものとするため、「Vibe Coding（後述する直感的なエージェント駆動開発手法）」の実践においては、以下の3つのMCPサーバーの併用が強く推奨されている12。

1. **Context-7 MCP:** プロジェクトで使用されている技術スタック（フレームワークやライブラリ）の最新のコードドキュメントやSDKリファレンスをエージェントに提供する12。これにより、非推奨のAPIが生成されるハルシネーションを抑制する。  
2. **Sequential Thinking MCP:** エージェントに対して、動的かつ内省的な問題解決プロセスを強制する12。これは構造化された思考プロセスを通じて、論理の飛躍を防ぎ、複数ステップにわたる難解なバグ修正や設計変更を安全に誘導する役割を担う6。  
3. **Retriever-based MCP (例: Qdrant MCP Server):** 過去に生成され、正常に動作したコードのベクトル表現を保存し、将来の類似タスクにおいて検索・再利用する機能を提供する12。これにより、プロジェクト特有のコーディング規約や設計パターンが組織の知識として蓄積・活用される。

これらのコードインテリジェンス系MCPサーバーの統合は、AIによるコード生成を「暗記に基づく確率的な予測」から「事実と構造に基づく決定論的なエンジニアリング」へと昇華させる重要な技術要素である。

## **自律的品質保証（Autonomous QA）とデプロイメントの包括的自動化**

AntigravityとMCPの連携がもたらす革新は、単なるコード記述の範疇を越え、システムの品質保証（QA）プロセスおよびインフラへのデプロイメント自動化にまで及んでいる。

### **TestSprite MCPによるE2Eテストの自律化**

AIによるコード生成において最も懸念されるのは、生成されたコードがエッジケースや統合環境下で正しく動作するかという品質の問題である。この課題に対し、TestSprite AI AgentのMCP ServerをAntigravityに統合することで、画期的な自律的テストワークフローが実現されている13。

従来、エンドツーエンド（E2E）テストの自動化には、PlaywrightやSeleniumといったフレームワークを用いて、人間が膨大なテストスクリプトを記述・保守する必要があった。しかしTestSprite MCP環境下では、エージェントがアプリケーションの仕様と生成されたコードを解析し、テストコードを人間が一行も書くことなしに、自律的にE2Eテストシナリオを生成・実行する13。 AIが最初に生成したコードは確率的モデルの性質上、一定のバグを含有しており、初期のテストパス率は42%程度に留まることが報告されている13。しかし、MCPを通じたテスト実行結果（エラーログやスタックトレース）が即座にエージェントへフィードバックされることで、エージェントは自己修復（セルフヒーリング）プロセスを開始する。コードの修正とテストの再実行という検証ループが人間の介入なしに高速回転した結果、最終的なAI生成コードの品質は93%のパス率へと劇的に向上するという実証データが示されている13。これは、ソフトウェア開発における品質保証プロセスが完全に自律化されたことを意味している。

### **UI/UX設計からReact生成、そしてクラウドデプロイへの直結**

アプリケーションのフロントエンド構築からデプロイメントに至る一連のライフサイクルも、MCPによって継ぎ目なく自動化されている。Googleが提供するAI駆動のUI/UXデザインエージェント「Stitch」をMCPサーバーとしてAntigravityに接続することで、プロンプト一つから完全なマルチページウェブサイト（例えばEコマースプラットフォームやフィットネス管理アプリケーション）を構築することが可能である14。Stitchの「Agent Skills」を活用することで、設計されたデザイン要件は即座にクリーンなReactコンポーネントコードへと自動変換される14。

生成されたアプリケーションを本番環境へ移行するデプロイメントフェーズは、コンテナ化や設定管理、サーバーハンドリングといった伝統的なインフラの壁が存在し、AI開発の俊敏性を阻害するボトルネックとなりがちである15。この摩擦を解消するため、Google Cloud Run MCP ServerやVercel、Netlify連携用のMCP環境が構築されている6。これにより、開発者はAntigravityのエディタ上から直接、Gemini CLIやエージェントに対して「このReactアプリケーションをCloud Runへデプロイせよ」と指示するだけで、インフラのプロビジョニングからデプロイまでのプロセスを完全に自律化できる15。

さらに、Firebase MCPサーバーを利用することで、バックエンドサービスとの連携も高度化される。このサーバーは、Cloud Firestoreのセキュリティルールの理解、Firebase Data Connectスキーマの取得、Firebase Cloud Messagingを用いたメッセージ送信ツールなどをエージェントに提供する17。これにより、エージェントは認証機能（Authentication）のセットアップやApp Hostingへのデプロイといった複雑なタスクを、プラットフォームのベストプラクティスに従った形で、エラーを最小限に抑えながら高精度に実行することが保証される17。

## **システム要件とAntigravity実行環境の整備**

これらの強力なエージェント能力とMCPのオーケストレーションを支えるためには、堅牢な基盤システムの構築が前提となる。Antigravityはローカルファイルシステムのパースや、マルチエージェントプロセス、サンドボックス化された環境内でのツール実行を伴うため、一般的なテキストエディタと比較して高いシステムリソースを要求する。

### **OS要件とハードウェア推奨スペック**

Antigravityは主要なデスクトップオペレーティングシステム間でクロスプラットフォーム対応を果たしているが、それぞれに明確な依存関係が存在する2。

以下の表は、各OSにおける最小要件および推奨ハードウェア要件を整理したものである。

| オペレーティングシステム | アーキテクチャと依存要件 |
| :---- | :---- |
| **Windows** | Windows 10 または Windows 11 (64-bit)。Intel/AMD向けのx64バージョンおよびQualcomm等向けのARM64バージョンが提供されている19。 **特記事項:** サンドボックス化されたターミナル実行のために「WSL2 (Windows Subsystem for Linux 2)」のインストールが必須要件である20。 |
| **macOS** | macOS バージョン12 (Monterey) 以降。Appleのセキュリティアップデートサポート対象バージョンであることが求められる。Apple Silicon (M1/M2/M3) 用およびIntel CPU用のパッケージがそれぞれ用意されている19。 |
| **Linux** | glibc \>= 2.28 および glibcxx \>= 3.4.25 をサポートするディストリビューション。具体的にはUbuntu 20以降、Debian 10、Fedora 36、RHEL 8などが該当する19。 |

ハードウェアリソースに関しては、複数の推論プロセスとMCPサーバーを並列稼働させるため、最小で8GBのRAMが必要とされるが、大規模なコードベースを扱う実践的なワークフローにおいては16GB以上のRAMが強く推奨される21。

### **ネットワークおよび認証基盤**

Antigravityはローカルクライアントでありながら、Google Cloudインフラストラクチャや最先端の推論API（Gemini 3 ProやClaude 4.5）と密接に連携するため、安定した高速インターネット環境（最低5Mbps以上）が不可欠である5。また、アプリケーションのUIテスト検証などを自動実行するための組み込みブラウザエージェントとして、最新バージョンのGoogle Chromeのインストールが要求される2。さらに、プロジェクト状態の同期やAPIへのアクセス認可のため、利用にあたってはPersonal GmailアカウントによるGoogle認証プロセスを完了させることが必須となっている2。

## **MCPサーバーの設定と高度な統合手法**

Antigravityに対するMCPサーバーの統合手法は、対象となるツールの提供形態に応じて、主に二つのアプローチが存在する。一つは組み込みの「MCP Store」を利用した安全で透過的なアプローチであり、もう一つは独自ツールやサードパーティバイナリを統合するための構成ファイル（mcp\_config.json）の直接編集アプローチである。

### **組み込みMCP Store経由の標準インストール**

最も推奨され、かつ摩擦の少ない導入手法は、エディタに内蔵されたMCP Storeを利用することである22。このプロセスは完全にUI駆動であり、手動による環境変数の設定ミスやバイナリパスの指定誤りを排除する1。

1. Antigravityのメインエディタ画面において、サイドパネルの「Agent」セクションを開く22。  
2. パネル上部に配置されているオプションメニュー（more\_horizアイコン / "..."ドロップダウン）をクリックし、「MCP Servers」を選択してストアインターフェースにアクセスする6。  
3. ストアには、BigQuery、AlloyDB、Firebase、GitHub、Notion、Linearなど数十種類の公式サポート対象サーバーがリストアップされている6。目的のサーバーを検索し、「Install」ボタンをクリックする1。  
4. 対象がGoogle Cloudのサービスや外部のSaaSである場合、画面上のプロンプトに従い、アカウントの認証やプロジェクトリソースへのアクセス権の承認プロセスを完了させる6。

インストールが完了した時点で、内部のmcp\_config.jsonファイルが自動的に更新され、エージェントは即座にそのサーバーが提供するコンテキストやツールを呼び出せる状態となる6。

### **mcp\_config.json を用いたカスタムサーバーの高度な構成**

公式ストアに登録されていないオープンソースのツールセット（例：n8n-mcp、Augment Context Engineなど）や、独自のローカルバイナリ（前述のGoatlasなど）、あるいはPythonスクリプト（NotebookLM連携など）をMCPサーバーとして立ち上げる場合、構成ファイルの直接編集（Raw config）による手動設定が必要となる12。

MCP Store上部の「Manage MCP Servers」メニューから「View raw config」を選択すると、ユーザーディレクトリ（例：Windows環境における C:\\Users\\\<USER\_NAME\>\\.gemini\\antigravity\\mcp\_config.json）に配置されたJSON設定ファイルがエディタ上で開かれる6。

設定ファイルの構造は、mcpServersというトップレベルのキー配下に、各サーバーの識別子と実行構成を定義する形式となっている。主要な設定パラメータは、起動コマンド（command）、コマンドライン引数（args）、およびプロセスの環境変数（env）で構成される。以下の表は、多様な環境下におけるカスタム設定の事例とその技術的意図を示したものである。

| 連携対象 | 構成記述例 (JSONスニペット) | 技術的設定意図と特徴 |
| :---- | :---- | :---- |
| **Augment Context Engine** (ローカルNPMパッケージの実行)23 | "augment-context-engine": { "command": "auggie", "args": \["--mcp", "--mcp-auto-workspace"\] } | グローバルインストールされたCLIツール（auggie）を直接呼び出し、ワークスペースのコンテキストを自動認識させる引数を付与している。 |
| **NotebookLM 連携** (Pythonスクリプトによるサーバー構築)25 | "notebooklm-mcp-server": { "command": "python", "args":, "env": { "PYTHONUNBUFFERED": "1" } } | 標準入力/出力（STDIO）をトランスポート層として利用するMCPにおいて、Pythonの出力バッファリングが原因で通信が遅延・ブロックされるのを防ぐため、-uフラグおよび環境変数でバッファリングを強制無効化している25。 |
| **Goatlas (AST解析)** (DB依存のローカルGoバイナリ)8 | "goatlas": { "command": "goatlas", "args": \["serve"\], "env": { "DATABASE\_DSN": "postgres://..." } } | ローカルのバイナリを実行しつつ、エージェントからは隠蔽されたセキュアな環境変数としてバックエンドのPostgreSQL接続文字列をサーバープロセスへ渡している8。 |

#### **ワークスペースパスの動的解決とプロセス分離の特性**

AntigravityにおけるMCP実装の極めて重要なアーキテクチャ上の特性として、各MCPプロセスがエディタプロセスから完全に分離（アイソレート）された状態でスポーンするという点がある27。これによりセキュリティと安定性は担保されるが、副作用として、MCPサーバー側からは自身が対象とすべき「現在のプロジェクトのベースディレクトリパス」を自動的に検知することが不可能となる27。

したがって、ローカルファイルシステムを走査するツールや、Jupyter Notebookを対象とするサーバー（antigravity-nbなど）を構成する場合、Antigravity固有の組み込み変数である ${workspaceFolder} を設定ファイルの引数（args）として明示的に渡し、サーバー側にパスを伝達しなければならない27。

JSON

"args": \["serve-agent", "--workspace-root", "${workspaceFolder}"\]

この記法を適用することで、複数のプロジェクトウィンドウが同時に開かれている環境下でも、パスの不整合や意図しないプロセスの爆発的増加を防ぎ、適切なディレクトリのコンテキストが各サーバープロセスへ安全に提供される27。

## **エージェントの自律的行動制御と Vibe Coding 実践論**

強力な推論能力と広範なMCPツールへのアクセス権を持つAIエージェントは、適切な制御を与えられなければ、不必要な探索を繰り返し、最終的にタスクの目的から逸脱する危険性を孕んでいる。トークンの消費を最適化し、エージェントを正しい方向へ導くためのフレームワークとして、システムプロンプトの設計と「Vibe Coding」と呼ばれる直感的ながら高度に体系化された開発プロセスの実践が不可欠となる。

### **AGENTS.md と Rules による厳格な行動統制**

Antigravityは、エージェントに対するメタ指示やプロジェクト固有の制約、コーディング標準を定義するための仕組みとして「Rules（またはSkills）」というコンセプトを採用している11。これはプロジェクト内にMarkdown形式のファイルとして配置され、エージェントがタスクに着手する際に必ず読み込まれる行動規範として機能する28。

具体的には、プロジェクトのルートディレクトリに配置された AGENTS.md や、.antigravity/rules.md、CONTEXT.md といったファイル群が連携し、システムアーキテクチャの基本方針や許容されるライブラリのバージョンなどを厳密に規定する30。例えば、業務自動化ツールであるn8nのMCP（n8n-mcp）を操作させる場合、以下のような指示を AGENTS.md に記述することで、劇的なパフォーマンス向上を図ることができる24。

* **サイレント実行（Silent Execution）の強制:** エージェントがツールを呼び出す際に「今から検索を実行します…完了しました！」といった不要な実況解説（コメント生成）を行うことは、トークンの浪費と遅延に直結する。これを防ぐため、「CRITICAL: ツール実行前の解説は厳禁とする。すべてのツールの実行が完了した後にのみ応答文を生成せよ」という制約を記述する24。  
* **並列実行（Parallel Execution）の最大化:** 独立したノード情報の取得やAPIコールにおいて、「操作が相互に依存していない場合は、パフォーマンス最大化のためにツールを並列実行（Parallel execution）することを必須とする」と明示することで、ネットワーク待機時間を最小化する24。

さらに、これらのスキルは特定のプロジェクトのみに適用される「ワークスペーススキル」と、すべてのプロジェクトに共通して適用される「グローバルスキル」に分類される29。開発者は、特定のフロントエンドデザインスキル（例えば画像生成ルールやタイポグラフィの制約など）をワークスペースで微調整した後、安定したものをグローバルに昇格させるという戦略的な運用が求められる29。

### **計画主導の Vibe Coding ワークフロー**

「Vibe Coding（直感コーディング）」という言葉の響きとは裏腹に、Antigravityを用いた開発プロセスは、厳密な「計画」を前提として成立する12。エージェントに突発的にコードを書かせるのではなく、以下の段階的なプロセスを経ることがベストプラクティスとして提唱されている。

1. **実装計画とワークフローの事前生成:** タスクの要件を定義した後、コードを記述させる前に、Gemini 3 Proエージェントに対して「Implementation Plan（実装計画）」「Task list（タスクリスト）」「Walkthrough（手順書）」の各ファイルを生成させる12。人間（開発者）はこれらのドキュメントを必ずレビューし、アーキテクチャの方針が間違っていないかを事前に検証する12。  
2. **自動テスト項目の除外によるコンテキスト保護:** 計画の中にエージェントによる自動化テストの実行ステップが含まれている場合、手動でこれを削除し、「テストは人間が手動で行うため、自律的なテスト実行は行わないこと」と指示を修正することが強く推奨される12。未熟なコードに対してエージェントがテストループに陥ると、トークンの消費が青天井になるリスクがあるためである（前述のTestSpriteのような専用QA用MCPを利用している場合を除く）12。  
3. **機能ブロックの細分化と段階的実装:** 5つ以上の機能を含むような大規模な実装を、一度のプロンプトでエージェントに要求することは避けるべきである12。機能を細分化し、一つ目の機能を完了させた段階で一旦プロセスを停止する12。  
4. **SUMMARY.md を用いた状態（ステート）の永続化:** ひとつのセッションが終了した時点で、エージェントに対してこれまでの文脈と決定事項を SUMMARY.md という要約ファイルとして出力させる12。次の機能開発に着手する際、このファイルをコンテキストとして読み込ませることで、初期設定やアーキテクチャ要件の説明をゼロからやり直すオーバーヘッドを完全に排除し、継続的な開発を実現する12。

## **運用上の制約、既知のシステム異常とトラブルシューティング**

Agent-firstの開発環境とMCPの統合は極めて強力であるが、システム自体が複雑なプロトコルスタックに依存しているため、特定の条件下で深刻なエラーを引き起こすことが確認されている。以下に、現在判明している主要な障害事例とその根本原因、および回避策を論じる。

### **STDIOプロトコルの非同期とフォーマットエラーの発生**

Antigravityの運用において最も深刻な技術的障害の一つが、「improper format stop reason」というエラーによるステップの即時クラッシュと、それに伴うセッション状態の永続的な破損である32。このエラーは、ネイティブツールのみを使用している環境では発生せず、PythonやNode.jsベースの外部MCPサーバー（主に標準入出力をトランスポートレイヤーとして利用するSTDIOベースのサーバー）がアクティブな状況下でのみ発生するという明確な相関関係が特定されている32。

**技術的根本原因:** 詳細な検証結果から、この障害の引き金は「複数ツールの並列実行」にあることが判明している32。エージェントが、Antigravityのネイティブなシステムツールである task\_boundary （ステップの区切りを管理するシンプルな文字列引数ツール）と、外部のMCPツール（例えばファイルの読み込みを行う view\_file など）を同一のターン内で並列に呼び出そうとした際、オーケストレーター内部でプロトコルの非同期化（Desynchronization）が発生する32。 具体的には、外部MCPサーバーの出力ストリーム（stdout/stderr）が漏洩し、プラットフォーム側がツール呼び出しを区切るために用いている内部の「制御トークン」とインターリーブ（混入・混在）してしまうことにより、推論モデルのグローバルJSONパーサーが構造を正しく解析できなくなり、クラッシュを引き起こすというメカニズムである32。興味深いことに、同一のタスクと環境設定であっても、Claude 3.5/4.5 Sonnetを利用した場合はこの問題が発生せず100%安定稼働したという報告があり、これはGeminiモデル特有のオーケストレーション・パースレイヤーにおける脆弱性であることが強く示唆されている32。

**回避策:** 恒久的なパッチが提供されるまでの暫定対応として、AGENTS.md にシステム指示を追加し、外部MCPサーバーが有効な状態においては、「task\_boundary を他のツールと並列で呼び出さず、必ず直列（シーケンシャル）で実行すること」をエージェントに厳格に強制することが有効な回避策となる32。

### **認証仕様の限界と環境依存の起動不全**

プロトコルの不具合に加え、認証機能の制約やOS特有のファイルシステムに関連するトラブルシューティングも、導入現場において重要な課題となっている。

1. **MCP OAuth仕様の非サポートによる認証ブロック:** 現行のAntigravity環境は、MCPが定めるOAuth仕様（MCP OAuth specifications）をサポートしていない33。このため、クライアントIDとクライアントシークレットを利用してユーザー認証やエージェントアイデンティティの確立を行う必要があるリモートMCPサーバーを設定した場合、エディタ上にツールリストは正常に表示されるものの、実行フェーズにおいて認証を通過できず、「Permission denied」等のエラー（例：Compute Engineの list\_images ツール実行時など）が返される33。現時点では、ローカル環境に保存されたApplication Default Credentials（ADC）や、env ブロックに直接APIキーを記述する認証方式を代替案として採用する必要がある17。  
2. **Windows環境におけるインストールパス依存のログインループ:** Windows版のAntigravityにおいて、アプリケーションが起動直後にログイン画面に戻されるループ現象や、「Agent terminated due to error」という致命的エラーで停止する事例が多数報告されている20。この問題の根本原因の大部分は、ディレクトリ権限やパス名解決の不具合にある。デフォルトのユーザーディレクトリ配下ではなく、管理者権限で明示的に C:\\Program Files\\Antigravity というパスへインストール先を変更することで、約70%のログインループ問題が解消されるという統計が示されている20。また、企業環境においては、グループポリシー（GPO）等を用いてこのパスへのインストールを標準化することが推奨される20。  
3. **WSL2の未稼働によるターミナルサイレント障害:** 前述の通り、Windows上でサンドボックス化されたターミナルをエージェントに操作させるにはWSL2が必須であるが、これが未インストール、またはバックグラウンドで稼働していない場合、ターミナルの操作がエラーメッセージを伴わずにサイレントに失敗し、エージェントが無限に待機状態に陥るケースがある20。wsl \--list \--verbose コマンドによる稼働状況の確認は、トラブルシューティングの初動として極めて重要である20。  
4. **サブスクリプション制限やネットワークに起因する切断:** エージェントが異常終了する原因が、MCPの実装やローカル環境のバグではなく、単なる「Google AI Proサブスクリプションの利用枠到達（1日または5時間あたりのリミット超過）」、あるいは一時的なネットワークの瞬断に起因しているケースも少なくない35。システムの再構築や設定ファイルの初期化（隠し設定フォルダの削除など）という重い作業を実行する前に、まずはアカウントのクォータとネットワークの導通確認を行うべきである34。

## **総括**

Google AntigravityとModel Context Protocol (MCP) の融合は、単なる「コードを生成するエディタ」の領域を遥かに越え、システム全体のコンテキストをリアルタイムで理解し操作する「自律的エンジニアリングプラットフォーム」への進化を決定づけるものである。本報告書での分析が示すように、エージェントがデータベースの実行計画からインフラのデプロイ、コードベースの抽象構文木（AST）、さらにはE2Eテストの自律的検証ループに至るまで、開発サイクルの全方位にわたって外部データとシームレスに接続可能となった意義は計り知れない。

その一方で、MCPの潜在能力を最大限に引き出すためには、無作為なテキスト検索に頼らないASTベースの解析サーバーの導入や、AGENTS.md を活用した緻密なプロンプトエンジニアリング（Vibe Codingの実践）、さらには設定ファイルの高度な記述といった人間側の「アーキテクトとしてのスキル」が新たに求められる。同時に、プロトコルレイヤーにおけるSTDIOの非同期エラーやOS固有の制約といった現存するシステムの脆弱性に対しても、的確な回避策を講じる運用知見が不可欠である。今後、エージェントファーストパラダイムの成熟に伴い、MCPエコシステムの統合手法とワークフローの最適化は、あらゆるソフトウェア開発組織において最重要の競争優位の源泉となることは疑いようがない。

#### **引用文献**

1. Connect Google Antigravity IDE to Google's Data Cloud services, 3月 21, 2026にアクセス、 [https://cloud.google.com/blog/products/data-analytics/connect-google-antigravity-ide-to-googles-data-cloud-services](https://cloud.google.com/blog/products/data-analytics/connect-google-antigravity-ide-to-googles-data-cloud-services)  
2. Getting Started with Google Antigravity, 3月 21, 2026にアクセス、 [https://codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)  
3. How to Set Up and Use Google Antigravity \- Codecademy, 3月 21, 2026にアクセス、 [https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity](https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity)  
4. Agent \- Google Antigravity Documentation, 3月 21, 2026にアクセス、 [https://antigravity.google/docs/agent](https://antigravity.google/docs/agent)  
5. How to Install and Setup Google Antigravity IDE on Windows 11 \- YouTube, 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=HKPIRY1fc5s](https://www.youtube.com/watch?v=HKPIRY1fc5s)  
6. Antigravity Editor: MCP Integration, 3月 21, 2026にアクセス、 [https://antigravity.google/docs/mcp](https://antigravity.google/docs/mcp)  
7. antigravity-workspace-template/docs/en/MCP\_INTEGRATION.md at main \- GitHub, 3月 21, 2026にアクセス、 [https://github.com/study8677/antigravity-workspace-template/blob/main/docs/en/MCP\_INTEGRATION.md](https://github.com/study8677/antigravity-workspace-template/blob/main/docs/en/MCP_INTEGRATION.md)  
8. Sharing my MCP setup — built a code intelligence server that cut Antigravity's search time from 30 tool calls to 1 : r/google\_antigravity \- Reddit, 3月 21, 2026にアクセス、 [https://www.reddit.com/r/google\_antigravity/comments/1ryt9hz/sharing\_my\_mcp\_setup\_built\_a\_code\_intelligence/](https://www.reddit.com/r/google_antigravity/comments/1ryt9hz/sharing_my_mcp_setup_built_a_code_intelligence/)  
9. Use Cloud SQL for MySQL with MCP, Gemini CLI, and other agents, 3月 21, 2026にアクセス、 [https://docs.cloud.google.com/sql/docs/mysql/pre-built-tools-with-mcp-toolbox](https://docs.cloud.google.com/sql/docs/mysql/pre-built-tools-with-mcp-toolbox)  
10. Decoding GCP Billing with Antigravity and BigQuery MCP | by Marcelo Costa | Google Cloud \- Community | Mar, 2026, 3月 21, 2026にアクセス、 [https://medium.com/google-cloud/decoding-gcp-billing-with-antigravity-and-bigquery-mcp-1941dd37ae09](https://medium.com/google-cloud/decoding-gcp-billing-with-antigravity-and-bigquery-mcp-1941dd37ae09)  
11. Tutorial : Getting Started with Google Antigravity Skills, 3月 21, 2026にアクセス、 [https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)  
12. Google Antigravity: How to add custom MCP server to improve Vibe Coding \- Medium, 3月 21, 2026にアクセス、 [https://medium.com/google-developer-experts/google-antigravity-custom-mcp-server-integration-to-improve-vibe-coding-f92ddbc1c22d](https://medium.com/google-developer-experts/google-antigravity-custom-mcp-server-integration-to-improve-vibe-coding-f92ddbc1c22d)  
13. TestSprite MCP Server \+ Google AntiGravity \= Autonomous E2E Testing (No Code Required\!), 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=ijMUgokpsqE](https://www.youtube.com/watch?v=ijMUgokpsqE)  
14. Antigravity \+ Stitch MCP: AI Agents That Build Complete Websites, 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=7wa4Ey\_tCCE](https://www.youtube.com/watch?v=7wa4Ey_tCCE)  
15. Deploy Applications from Gemini CLI and Antigravity to Cloud Run using MCP Server, 3月 21, 2026にアクセス、 [https://codelabs.developers.google.com/deploy-to-cloud-run-using-oss-mcp-server](https://codelabs.developers.google.com/deploy-to-cloud-run-using-oss-mcp-server)  
16. Connect Antigravity to GitHub: The Complete MCP Setup \- YouTube, 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=7wlhtf9Kqk0](https://www.youtube.com/watch?v=7wlhtf9Kqk0)  
17. Firebase MCP server | Develop with AI assistance \- Google, 3月 21, 2026にアクセス、 [https://firebase.google.com/docs/ai-assistance/mcp-server](https://firebase.google.com/docs/ai-assistance/mcp-server)  
18. What technical requirements do I need for Google Antigrav... \- LinkGo, 3月 21, 2026にアクセス、 [https://linkgo.dev/faq/technical-requirements-i-need-for-google-antigravity](https://linkgo.dev/faq/technical-requirements-i-need-for-google-antigravity)  
19. Google Antigravity — Set Up Guide | by Mayur Jain | Medium, 3月 21, 2026にアクセス、 [https://mayur-ds.medium.com/google-antigravity-set-up-guide-c15f8df80c6c](https://mayur-ds.medium.com/google-antigravity-set-up-guide-c15f8df80c6c)  
20. Antigravity Not Working? 10 Common Issues & Fixes \- Skywork ai, 3月 21, 2026にアクセス、 [https://skywork.ai/blog/agent/antigravity-not-working/](https://skywork.ai/blog/agent/antigravity-not-working/)  
21. 3月 21, 2026にアクセス、 [https://www.antigravityide.help/docs](https://www.antigravityide.help/docs)  
22. Use Spanner with MCP Toolbox for Databases, Gemini CLI, and other agents, 3月 21, 2026にアクセス、 [https://docs.cloud.google.com/spanner/docs/pre-built-tools-with-mcp-toolbox](https://docs.cloud.google.com/spanner/docs/pre-built-tools-with-mcp-toolbox)  
23. AntiGravity Quickstart \- Augment, 3月 21, 2026にアクセス、 [https://docs.augmentcode.com/context-services/mcp/quickstart-anti-gravity](https://docs.augmentcode.com/context-services/mcp/quickstart-anti-gravity)  
24. n8n-mcp/docs/ANTIGRAVITY\_SETUP.md at main \- GitHub, 3月 21, 2026にアクセス、 [https://github.com/czlonkowski/n8n-mcp/blob/main/docs/ANTIGRAVITY\_SETUP.md](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/ANTIGRAVITY_SETUP.md)  
25. NotebookLM MCP Server for Antigravity \- LobeHub, 3月 21, 2026にアクセス、 [https://lobehub.com/mcp/duykhanhbv-bit-notebooklm-mcp-antigravity](https://lobehub.com/mcp/duykhanhbv-bit-notebooklm-mcp-antigravity)  
26. Connect to the Developer Knowledge MCP server \- Google for Developers, 3月 21, 2026にアクセス、 [https://developers.google.com/knowledge/mcp](https://developers.google.com/knowledge/mcp)  
27. Please provide ENV for current project base dir to MCP servers \- Google Antigravity, 3月 21, 2026にアクセス、 [https://discuss.ai.google.dev/t/please-provide-env-for-current-project-base-dir-to-mcp-servers/119313](https://discuss.ai.google.dev/t/please-provide-env-for-current-project-base-dir-to-mcp-servers/119313)  
28. Rules / Workflows \- Google Antigravity Documentation, 3月 21, 2026にアクセス、 [https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)  
29. Antigravity Skills Give You an Unfair Advantage, 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=EIFrH0JDXnA](https://www.youtube.com/watch?v=EIFrH0JDXnA)  
30. AGENTS.md, 3月 21, 2026にアクセス、 [https://agents.md/](https://agents.md/)  
31. AGENTS.md \- study8677/antigravity-workspace-template \- GitHub, 3月 21, 2026にアクセス、 [https://github.com/study8677/antigravity-workspace-template/blob/main/AGENTS.md](https://github.com/study8677/antigravity-workspace-template/blob/main/AGENTS.md)  
32. Bug Report: Antigravity Tool-Calling Failure ("Improper Format Stop Reason") \- Google Help, 3月 21, 2026にアクセス、 [https://support.google.com/gemini/thread/405322994/bug-report-antigravity-tool-calling-failure-improper-format-stop-reason?hl=en](https://support.google.com/gemini/thread/405322994/bug-report-antigravity-tool-calling-failure-improper-format-stop-reason?hl=en)  
33. Known issues | Google Cloud MCP servers, 3月 21, 2026にアクセス、 [https://docs.cloud.google.com/mcp/known-issues](https://docs.cloud.google.com/mcp/known-issues)  
34. How to Fix “Agent Terminated Due to Error” in Google Anti‑Gravity \- YouTube, 3月 21, 2026にアクセス、 [https://www.youtube.com/watch?v=s7MwugdES9Y](https://www.youtube.com/watch?v=s7MwugdES9Y)  
35. AntiGravity Agent terminated due to error, You can prompt the model to try again or start a new conversation if the error persists : r/Bard \- Reddit, 3月 21, 2026にアクセス、 [https://www.reddit.com/r/Bard/comments/1ph6g7d/antigravity\_agent\_terminated\_due\_to\_error\_you\_can/](https://www.reddit.com/r/Bard/comments/1ph6g7d/antigravity_agent_terminated_due_to_error_you_can/)