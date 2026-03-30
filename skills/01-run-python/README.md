# 01-run-python

この文書は、`01-run-python` サンプルの概要と最小実行例だけをまとめたものです。
共通の配置方法、OpenClaw からの認識確認、TUI / WebDashboard / Discord でのテスト手順は [README.md](../../README.md) を参照してください。

## このサンプルがやること

- 地名や施設名から Google Maps の検索 URL を生成する
- 返却値を JSON で返す
- Python 標準ライブラリだけで動かす

## 想定する利用場面

- 東京駅を Google Maps で開きたい
- 大阪城の地図 URL を返したい
- Discord や TUI から場所検索用の URL だけを簡潔に返したい

## 関連文書

- [../../README.md](../../README.md): リポジトリ全体の導入、配置、認識確認、共通テスト手順
- [SKILL.md](SKILL.md): OpenClaw が実行時に参照する Skill 定義
- [../../docs/01-run-python.md](../../docs/01-run-python.md): TUI 用プロンプト例と設計メモ

## ファイル構成

- `SKILL.md`: Skill の用途、実行方法、返答方針を定義する
- `scripts/place_to_gmap.py`: 入力文字列から Google Maps 検索 URL を生成する

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
{"ok": true, "query": "東京駅", "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"}
```

## 動作確認の観点

このサンプルの確認では、Google Maps 上でどの候補が開くかまでは評価対象にしません。
確認すべきなのは、スクリプトが次の最小 JSON 契約を守っているかです。

- `ok`
- `query`
- `map_url`

逆に、`label`、`center`、`zoom` のような追加情報はこのサンプルの仕様外です。
WebDashboard やチャットで補足情報つきに見える場合があっても、スクリプト本体の仕様確認とは分けて扱います。

## 補足

- 実行時の応答方針や Safety Defaults は [SKILL.md](SKILL.md) に記載しています
- このサンプルを OpenClaw TUI で生成するための指示例は [../../docs/01-run-python.md](../../docs/01-run-python.md) にまとめています
- スクリプトの実行ログは標準エラーに JSON Lines で出力されます
- 既定では `~/.openclaw/workspace/logs/skills/01-run-python.jsonl` にも追記されます

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

保存先を変えたい場合:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --log-file /tmp/01-run-python.jsonl 東京駅
```

ファイルへ残さず標準エラーだけにしたい場合:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --no-file-log 東京駅
```
