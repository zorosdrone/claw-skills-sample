
# 01-run-python を生成するためのプロンプト集

この文書は、`01-run-python` を OpenClaw TUI で生成したいときのプロンプト例と、その意図をまとめたものです。
サンプルの概要と実行例は [../skills/01-run-python/README.md](../skills/01-run-python/README.md)、実行時の定義は [../skills/01-run-python/SKILL.md](../skills/01-run-python/SKILL.md)、共通の配置とテスト手順は [../README.md](../README.md) を参照してください。

## 生成対象

作成対象の最小構成:

- `skills/01-run-python/SKILL.md`
- `skills/01-run-python/scripts/place_to_gmap.py`

固定したい要件:

- 地名や施設名を受け取り、Google Maps の検索 URL を返す
- 返却は JSON とする
- JSON には `ok`, `execution_id`, `query`, `map_url` を含める
- `SKILL.md` の frontmatter の `name` は `01-run-python` にする
- Python 標準ライブラリのみ使う
- 地名未指定時はエラー JSON を返す

検証時に固定したい観点:

- 動作確認は Google Maps 上の候補確定ではなく、JSON の形が仕様どおりかで判断する
- `label`, `center`, `zoom` などの追加情報はこの最小サンプルでは要求しない

## 推奨プロンプト例

```text
OpenClaw の skill を作って。
配置先は skills/01-run-python/ にして。

必要ファイル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

要件:
- 地名や施設名を受け取り、Google Maps の検索 URL を返す
- 返却は JSON にする
- JSON には ok, query, map_url を含める
- SKILL.md の frontmatter の name は 01-run-python にする
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
- --query オプションで地名を受け取れる
- 位置引数でも地名を受け取れる
- どちらも無いときはエラー
- 成功時は Google Maps の search URL を生成して JSON を出力する

まずは最小構成で動くところまで作って。
```

## 短いプロンプト例

```text
skills/01-run-python/ に OpenClaw の skill を作って。

必要ファイル:
- skills/01-run-python/SKILL.md
- skills/01-run-python/scripts/place_to_gmap.py

要件:
- 地名から Google Maps 検索 URL を作る
- JSON で ok, execution_id, query, map_url を返す
- SKILL.md の name は 01-run-python
- Python 標準ライブラリのみ使う
- 地名未指定時はエラー JSON を返す

最小構成でまず動くものを作って。
```

## 生成後の確認ポイント

- `SKILL.md` の frontmatter の `name` が `01-run-python` になっているか
- 実行コマンド例が `skills/01-run-python/...` になっているか
- スクリプトが JSON を返すか
- 配置、認識確認、テスト手順は [../README.md](../README.md) の流れで確認できるか