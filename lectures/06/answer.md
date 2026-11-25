# 第6回 解答



## 演習

- STEP 1 のツールの名前：
  - 通常起動：search_materials
  - MCP起動：glossary_search_glossary
  - 要約ツール追加後：glossary_get_lecture_summary
  - fetchサーバー追加後：fetch_fetch
- STEP 2 の [tool call]：
  [tool call]   glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：
  [tool call]   glossary_get_lecture_summary({'lecture': 2})
- STEP 4 の [tool call]：
  [tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- 気づき・疑問：
  MCPのツール名には glossary_ や fetch_ というサーバー名が付いていた。モデルには、ツールの名前・説明文・引数が渡されていた。get_lecture_summary はサーバーへの登録を1行追加すると使えるようになり、fetch は設定ファイルへの追加で利用できた。fetch実行時には、公式サイトへのHTTPアクセスと、その内容を使った日本語3行の要約を確認できた。テストは21件すべて合格した。

## 宿題

- 取り組んだレベル：基礎
- やったこと：
  用語集サーバーを `uv run python -m app.mcp_server --http` で起動し、app/mcp_servers.json の glossary を `{"url": "http://127.0.0.1:8000/mcp"}` に変更した。同じ「第2回では何を学びますか？」という質問で、stdioとStreamable HTTPの動作を確認した。
  さらに、app/tools.py の get_lecture_summary のdocstringに、講義全体の内容や学習目標を聞かれたらこのツールを優先することと、lectureに指定する整数の例を追加した。保存後にHTTPサーバーを再起動し、--list-tools と --trace で変更を確認した。
- 結果：
  stdioでは、設定のcommandとargsを使ってエージェントがサーバーを子プロセスとして起動し、標準入出力で通信した。HTTPでは、別ターミナルでサーバーを起動しておき、エージェントがポート8000の /mcp に接続した。HTTP側のログには、POSTやGETなどの通信が表示された。
  docstringの変更後、--list-tools に「このツールを優先して使う」という新しい説明と、lectureの指定例が表示された。変更前後とも、glossary_get_lecture_summary に lecture: 2 を渡して1回呼び出し、第2回の要点を回答した。モデル応答回数は2回だった。

| 項目 | HTTP・説明文変更前 | HTTP・説明文変更後 |
|---|---|---|
| ツール呼び出し | glossary_get_lecture_summary、lecture: 2、1回 | glossary_get_lecture_summary、lecture: 2、1回 |
| 回答時間 | 8.73秒 | 7.24秒 |
| 入力トークン数 | 1,992 | 2,062 |
| 出力トークン数 | 438 | 443 |
| モデル応答回数 | 2回 | 2回 |
| 生成API推定費用 | $0.001693 | $0.001726 |

- 気づき・疑問：
  stdioとHTTPでは、サーバーを起動する担当と通信方法が異なるが、同じツールを呼び出して回答できた。HTTPサーバーは起動後に接続を待つため、クライアントのコマンドは別のターミナルで実行する必要があった。また、docstringを保存しても、起動済みのサーバーには再起動するまで変更が反映されなかった。
  説明文はモデルに渡されるツールの情報になる。今回の質問では変更前から適切なツールが選ばれており、変更後も呼び出し方は同じだった。各条件1回の結果なので、回答時間の差が説明文の変更によるものかは判断できない。