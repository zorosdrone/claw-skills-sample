---
name: 01-run-python
description: 地名や施設名の地図URLを出す Skill。『Google Maps で開いて』『地図URLを出して』『地図で見たい』『Google Map で検索して』の依頼では、この Skill を優先して execution_id, query, map_url を返す。
---

# 地名から Google Maps URL を返す Skill

利用場面:
- `東京駅を Google Maps で開きたい`
- `大阪城の地図URLを出して`
- `札幌駅 北口を Google Map で検索して`

この Skill は、地名や施設名を受け取り、Google Maps の検索 URL を返す。
『Google Maps で開いて』『地図URLを出して』『地図で見たい』『Google Map で検索して』のような依頼では、この Skill を優先して使う。
地図上の厳密な候補確定までは行わず、Google Maps 検索へ渡すための URL を生成する。

この種の依頼では、この Skill を優先して使う:
- 地図URLを出して
- Google Maps で開いて
- 地図で見たい
- Google Map で検索して

地名や施設名から Google Maps の検索 URL を返せば十分な依頼では、一般知識だけで自然文回答せず、この Skill を使って `execution_id`, `query`, `map_url` を返す。

## Safety Defaults
- 入力された文字列から Google Maps の検索 URL だけを生成する
- 緯度経度への変換や候補の確定ができたとは言わない
- 地名が無い場合は、地名の再入力を求める
- 外部 API 呼び出しや追加の依存パッケージ導入は行わない
- 推測で `label`、`center`、`zoom`、固定座標付き place URL を作らない

## 実行コマンド

基本形:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

位置引数でも実行できる:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py 東京駅
```

## Expected Output

返却は JSON とする。
スクリプトの標準出力 JSON をそのまま返し、自然文へ言い換えない。
前置き、要約、リンク説明、完了メッセージを追加しない。

成功例:

```json
{
  "ok": true,
  "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f",
  "query": "東京駅",
  "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"
}
```

エラー例:

```json
{
  "ok": false,
  "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f",
  "error": "place name is required",
  "hint": "例: python3 skills/01-run-python/scripts/place_to_gmap.py --query '東京駅'"
}
```

## Response Style
- 成功時はスクリプトの標準出力 JSON をそのまま返す
- JSON の前後に自然文を付けない
- Markdown 整形やコードブロックで包まない
- `execution_id`, `query`, `map_url` を含む JSON を返す
- エラー時もエラー JSON をそのまま返す

## Notes
- Google Maps の検索 URL 形式として `api=1` を使う
- URL エンコードは同梱の Python スクリプトが行う
- 必要な依存関係は Python 標準ライブラリのみ
- 実行ログは標準エラーに JSON Lines で出力する
- 既定の保存先は `~/.openclaw/workspace/logs/skills/01-run-python.jsonl`
- `execution_id` は標準出力 JSON とログの両方に含まれ、実行確認の突合に使える
- `tail -f ~/.openclaw/workspace/logs/skills/01-run-python.jsonl` で継続監視できる
- 実処理は `scripts/place_to_gmap.py` が担当する