
# 01-run-python を生成するためのプロンプト集

この文書は、`01-run-python` を OpenClaw TUI で生成したいときのプロンプト例と、その意図をまとめたものです。
サンプルの概要と実行例は [../skills/01-run-python/README.md](../skills/01-run-python/README.md)、実行時の定義は [../skills/01-run-python/SKILL.md](../skills/01-run-python/SKILL.md)、共通の配置とテスト手順は [../README.md](../README.md) を参照してください。

## この文書の役割

- OpenClaw TUI に渡すプロンプト例を残す
- どの要件を固定すると生成が安定するかを記録する
- 生成時に確認すべきポイントを整理する

## 生成対象

作成対象の最小構成:

- `skills/01-run-python/SKILL.md`
- `skills/01-run-python/scripts/place_to_gmap.py`

固定したい要件:

- 地名や施設名を受け取り、Google Maps の検索 URL を返す
- 返却は JSON とする
- JSON には `ok`, `query`, `map_url` を含める
- `SKILL.md` の frontmatter の `name` は `01-run-python` にする
- Python 標準ライブラリのみ使う
- 地名未指定時はエラー JSON を返す

検証時に固定したい観点:

- 動作確認は Google Maps 上の候補確定ではなく、JSON の形が仕様どおりかで判断する
- `label`, `center`, `zoom` などの追加情報はこの最小サンプルでは要求しない

## 長いプロンプト例

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
- JSON で ok, query, map_url を返す
- SKILL.md の name は 01-run-python
- Python 標準ライブラリのみ使う
- 地名未指定時はエラー JSON を返す

最小構成でまず動くものを作って。
```

## Discord を意識したプロンプト例

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
- JSON は ok, query, map_url を含める
- エラー時は短い理由を返す
- Python 標準ライブラリのみ使う
- SKILL.md の name はフォルダー名と同じ 01-run-python

Discord での返答方針も SKILL.md に書いて。
簡潔でぶれない最小構成にして。
```

## この文書で残す理由

- 配置先を `skills/01-run-python/` まで明示すると生成のぶれが減る
- 必要ファイルを固定すると、余計な補助ファイルを作りにくくなる
- JSON キーを固定すると、出力形式のぶれを抑えられる
- `name` とフォルダ名を一致させると、運用時の混乱を避けやすい

## 生成後の確認ポイント

- `SKILL.md` の frontmatter の `name` が `01-run-python` になっているか
- 実行コマンド例が `skills/01-run-python/...` になっているか
- スクリプトが JSON を返すか
- 配置、認識確認、テスト手順は [../README.md](../README.md) の流れで確認できるか