# 01-run-python

この文書は、`01-run-python` サンプルの概要と最小実行例だけをまとめたものです。
共通の配置方法、OpenClaw からの認識確認、TUI / WebDashboard / Discord でのテスト手順は [README.md](../../README.md) を参照してください。

## このサンプルがやること

- 地名や施設名から Google Maps の検索 URL を生成する
- 返却値を JSON で返す
- Python 標準ライブラリだけで動かす

## 関連文書

- [../../README.md](../../README.md): リポジトリ全体の導入、配置、認識確認、共通テスト手順
- [SKILL.md](SKILL.md): OpenClaw が実行時に参照する Skill 定義
- [../../docs/01-run-python.md](../../docs/01-run-python.md): TUI 用プロンプト例と設計メモ

## 最小実行例

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

位置引数でも実行できます。

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py 東京駅
```

## 出力例

```json
{"ok": true, "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f", "query": "東京駅", "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"}
```

## 確認する項目

- `ok`
- `execution_id`
- `query`
- `map_url`

`label`、`center`、`zoom` のような追加情報はこのサンプルの仕様外です。

## 補足

- スクリプトの実行ログは標準エラーに JSON Lines で出力されます
- 既定では `~/.openclaw/workspace/logs/skills/01-run-python.jsonl` にも追記されます
- `execution_id` は標準出力 JSON とログの両方に入り、同一実行の突合に使えます

## ログの確認方法

直近のログを確認する:

```bash
tail -n 20 ~/.openclaw/workspace/logs/skills/01-run-python.jsonl
```

継続監視する:

```bash
tail -f ~/.openclaw/workspace/logs/skills/01-run-python.jsonl
```

エラーだけ見る:

```bash
grep '"stage": "error"' ~/.openclaw/workspace/logs/skills/01-run-python.jsonl
```

特定の実行を追う:

```bash
grep '"execution_id": "<応答に出た execution_id>"' ~/.openclaw/workspace/logs/skills/01-run-python.jsonl
```

保存先を変えたい場合:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --log-file /tmp/01-run-python.jsonl 東京駅
```

ファイルへ残さず標準エラーだけにしたい場合:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --no-file-log 東京駅
```
