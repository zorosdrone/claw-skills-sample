
TUIへのコマンド
地名からGoogleMapを検索してヒットした場所を開くURLを返す。SKILLを作って。

作成したサンプル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

概要:
- 地名や施設名を受け取り、Google Maps の検索 URL を JSON で返す
- Python 標準ライブラリのみで動作
- OpenClaw の skills 配下に配置すれば、そのまま再利用可能

実行例:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

想定出力:

```json
{"ok":true,"query":"東京駅","map_url":"https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"}
```

SKILL.md の解説:

- `---` から `---` までの frontmatter は、OpenClaw が Skill を識別するためのメタ情報
- `name: 01-run-python` はフォルダー名と一致させると管理しやすい
- `description` には、この Skill をどんな依頼で使うかを書く

各セクションの役割:

- `# Place To Google Maps`
	Skill の人間向けタイトル
- `Use this skill when ...`
	どのような依頼でこの Skill を使うべきかを示す
- `## Safety Defaults`
	Skill が勝手にやってはいけないこと、曖昧なときの扱いを書く
- `## Command`
	実際に呼び出すスクリプトと引数の例を書く
- `## Expected Output`
	返却される JSON の形を明示する
- `## Response Style`
	OpenClaw やチャットでどう返答するかの方針を書く
- `## Notes`
	実装上の補足や依存関係の有無を書く

このサンプルでのポイント:

- SKILL.md 自体は処理本体ではなく、Skill の使い方と運用ルールを定義する説明書
- 実際の処理は `scripts/place_to_gmap.py` が担当する
- つまり役割分担は `SKILL.md = 使い方の定義`、`Python スクリプト = 実処理`

見る順番のおすすめ:

1. SKILL.md の `description` で用途を確認する
2. `## Command` で実行方法を見る
3. `## Expected Output` で返却 JSON を確認する
4. 必要なら `scripts/place_to_gmap.py` を読んで実装を追う

OpenClaw TUI に貼るプロンプト例:

```text
OpenClaw の skill を作って。
配置先は skills/01-run-python/ にして。

必要ファイル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

要件:
- 地名や施設名を受け取り、Google Maps の検索 URL を返す
- 返却は JSON にする
- JSON には `ok`, `query`, `map_url` を含める
- `SKILL.md` の frontmatter の `name` は `01-run-python` にする
- Python 標準ライブラリのみ使う
- URL エンコードを行う
- 地名が未指定ならエラー JSON を返す

SKILL.md には以下を書く:
- この skill を使う場面
- Safety Defaults
- 実行コマンド例
- Expected Output
- Response Style
- Notes

Python スクリプトの仕様:
- `--query` オプションで地名を受け取れる
- 位置引数でも地名を受け取れる
- どちらも無いときはエラー
- 成功時は Google Maps の search URL を生成して JSON を出力する

まずは最小構成で動くところまで作って。
```

このプロンプトが通りやすい理由:

- 配置先を `skills/01-run-python/` まで明示している
- 必要ファイルを先に固定している
- `name` とフォルダー名の一致条件を明示している
- JSON のキーを固定して、出力ぶれを減らしている
- 「最小構成で動くところまで」と書いて、余計な拡張を防いでいる

補足:

- OpenClaw TUI が毎回そのまま完全生成する保証はない
- ただし、この粒度で指示すると雛形生成はかなり安定しやすい
- 生成後は `SKILL.md` の `name`、配置先、実行コマンドを最後に人が確認するのが安全

OpenClaw TUI 用の短いプロンプト例:

```text
skills/01-run-python/ に OpenClaw の skill を作って。

必要ファイル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

要件:
- 地名から Google Maps 検索 URL を作る
- JSON で `ok`, `query`, `map_url` を返す
- `SKILL.md` の `name` は `01-run-python`
- Python 標準ライブラリのみ使う
- 地名未指定時はエラー JSON を返す

最小構成でまず動くものを作って。
```

Discord 経由を意識したプロンプト例:

```text
Discord から使いやすい OpenClaw の skill を作って。
配置先は skills/01-run-python/ 。

目的:
- 地名を受け取って Google Maps の URL を返す

必要ファイル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

仕様:
- 入力は地名や施設名
- 出力は JSON
- JSON は `ok`, `query`, `map_url` を含める
- エラー時は短い理由を返す
- Python 標準ライブラリのみ使う
- `SKILL.md` の `name` はフォルダー名と同じ `01-run-python`

Discord での返答方針も `SKILL.md` に書いて。
簡潔でぶれない最小構成にして。
```

使い分け:

- 最初の長い版は、生成のぶれを最小化したいときに向く
- 短い版は、まず雛形だけ素早く作らせたいときに向く
- Discord 版は、応答の短さや JSON 形式まで意識させたいときに向く