# 01-run-python

このサンプルは、地名や施設名を受け取って Google Maps の検索 URL を返す OpenClaw Skill です。
最小構成の Skill として、SKILL.md に使い方と運用ルールを書き、Python スクリプトで実処理を行います。

## できること

- 地名や施設名から Google Maps の検索 URL を生成する
- 返却値を JSON で統一する
- Python 標準ライブラリだけで動かす

## 想定する利用場面

- 東京駅を Google Maps で開きたい
- 大阪城の地図 URL を返したい
- Discord や TUI から場所検索用の URL だけを簡潔に返したい

## ファイル構成

- SKILL.md: この Skill をいつ使うか、どう返すか、何をしないかを定義する
- scripts/place_to_gmap.py: 入力文字列から Google Maps 検索 URL を生成する

## 実行例

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

または位置引数でも実行できます。

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py 東京駅
```

## 出力例

```json
{"ok": true, "query": "東京駅", "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"}
```

## このサンプルのポイント

- Skill の説明と実処理を分けた最小構成になっている
- 出力形式が JSON なので他の処理から扱いやすい
- OpenClaw の Skill 作成時に必要な基本要素をひと通り含んでいる
