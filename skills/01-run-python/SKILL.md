---
name: 01-run-python
description: 地名や施設名から Google Maps の検索 URL を生成して JSON で返す Skill。場所を地図で開きたい依頼に使う。
---

# 地名から Google Maps URL を返す Skill

利用場面:
- `東京駅を Google Maps で開きたい`
- `大阪城の地図URLを出して`
- `札幌駅 北口を Google Map で検索して`

この Skill は、地名や施設名を受け取り、Google Maps の検索 URL を返す。
地図上の厳密な候補確定までは行わず、Google Maps 検索へ渡すための URL を生成する。

## Safety Defaults
- 入力された文字列から Google Maps の検索 URL だけを生成する
- 緯度経度への変換や候補の確定ができたとは言わない
- 地名が無い場合は、地名の再入力を求める
- 外部 API 呼び出しや追加の依存パッケージ導入は行わない

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

成功例:

```json
{
  "ok": true,
  "query": "東京駅",
  "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"
}
```

エラー例:

```json
{
  "ok": false,
  "error": "place name is required",
  "hint": "例: python3 skills/01-run-python/scripts/place_to_gmap.py --query '東京駅'"
}
```

## Response Style
- 単純な依頼なら URL をそのまま返す
- 必要なら元の検索語も一緒に返す
- エラー時は短い理由と再入力例を返す
- Discord やチャットでは冗長な説明を避け、短く返す

## Notes
- Google Maps の検索 URL 形式として `api=1` を使う
- URL エンコードは同梱の Python スクリプトが行う
- 必要な依存関係は Python 標準ライブラリのみ
- 実処理は `scripts/place_to_gmap.py` が担当する