# claw-skills-sample
OpenClawのSKILL学習用プロジェクト。
目標：日本語でのArdupilotSITL上のドローンに指示を出せる事

サンプル一覧:
- skills/01-run-python: 地名から Google Maps 検索 URL を返す最小 SKILL サンプル

参考プロジェクト
・https://github.com/zorosdrone/claw-sitl-ops


前提:
- XServer 無料VPS 上で OpenClaw を常駐
- 最新版 OpenClaw を利用
- Tailscale 稼働済み
- Discord 連携も想定
- ArdupilotSITLはWindowsPCのWSLで動かす
- WindowsPC/WSL側にもTailScale導入済み
- このプロジェクトはOpenClawが動いているマシンで開発されている

## 開発、検証環境構築

このリポジトリは、OpenClaw で利用する Skill の最小構成を確認するためのサンプル集です。
各 Skill は `skills/` 配下に配置し、`SKILL.md` と必要なスクリプト群をセットで管理します。

## Skill の配置方法

OpenClaw で Skill を認識させるには、各 Skill を `skills/<skill_name>/` 配下に配置します。

最小構成の例:

```text
skills/
	01-run-python/
		README.md
		SKILL.md
		scripts/
			place_to_gmap.py
```

配置時の考え方:

- `skills/<skill_name>/SKILL.md` に Skill の説明、用途、実行方法を書く
- 実際の処理は `skills/<skill_name>/scripts/` 配下に置く
- `SKILL.md` の frontmatter は Skill の識別に使うため、内容を明確に書く
- 新しい Skill を追加するときも同じ構成を踏襲すると管理しやすい

現在のサンプル:

- `skills/01-run-python`: 地名や施設名から Google Maps 検索 URL を返す Skill

## Skill 配置後に有効であることを確認する手順

Skill を `skills/` 配下に配置した後は、OpenClaw から認識されていることを確認します。
OpenClaw CLI で参照する Skill 名は、ディレクトリ名ではなく `SKILL.md` の frontmatter にある `name` を使います。
このサンプルではディレクトリ名と Skill 名をどちらも `01-run-python` に揃えています。

1. 利用可能な Skill 一覧を表示する

```bash
openclaw skills list
```

確認ポイント:

- `01-run-python` が一覧に表示されること
- Skill 名や説明が崩れていないこと

2. 対象 Skill の詳細を確認する

```bash
openclaw skills info 01-run-python
```

確認ポイント:

- 対象 Skill の情報が取得できること
- `SKILL.md` が正しく読まれていること

3. Skill の readiness を確認する

```bash
openclaw skills check
```

必要なら詳細表示:

```bash
openclaw skills check --verbose
```

確認ポイント:

- 対象 Skill が ready として扱われること
- 足りない要件があれば `--verbose` で内容を確認できること

表示されない場合の確認項目:

- ディレクトリが `skills/01-run-python/` になっているか
- `SKILL.md` がその直下にあるか
- `SKILL.md` の frontmatter が壊れていないか
- `name` や説明の記述に不整合がないか
- `openclaw skills info` にはディレクトリ名ではなく frontmatter の `name` を渡しているか

一覧で確認できた後に、TUI や WebDashboard から実際に呼び出して動作確認へ進みます。

## テスト方法

このプロジェクトでは、少なくとも以下の 4 通りで検証できます。

事前条件:

- OpenClaw の Gateway が起動していること
- Gateway が未起動の場合は、別ターミナルで次を実行する

```bash
openclaw gateway
```

ポート競合などで再起動したい場合:

```bash
openclaw gateway --force
```

## 1. コマンドラインからのテスト

まずはスクリプト単体で正しい JSON が返ることを確認します。

実行例:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

期待される出力例:

```json
{"ok": true, "query": "東京駅", "map_url": "https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85"}
```

確認ポイント:

- `ok` が `true` であること
- `query` に入力した文字列が入ること
- `map_url` に Google Maps の検索 URL が入ること

未入力時の確認例:

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py
```

この場合はエラー JSON が返ることを確認します。

## 2. TUI からのテスト

OpenClaw の TUI から、Skill が自然言語の依頼に応答できるか確認します。

起動方法:

```bash
openclaw tui
```

補足:

- 既定では現在の Gateway 設定に接続する
- 返信を実際のチャネルへ配送したい構成では `--deliver` を付けて起動できる
- 初回接続時に Gateway が見つからない場合は、先に `openclaw gateway` を起動する

確認例:

- 東京駅を Google Maps で開きたい
- 大阪城の地図 URL を出して
- 札幌駅 北口を Google Map で検索して

確認ポイント:

- `01-run-python` の Skill が選ばれること
- URL だけ、または簡潔な説明つきで返答されること
- 地図候補を確定したとは言わず、検索 URL を返していること

## 3. WebDashboard からのテスト

OpenClaw の WebDashboard から同様の依頼を送り、Web UI 上でも同じ挙動になることを確認します。

起動方法:

```bash
openclaw dashboard
```

ブラウザを自動で開かず、URL だけ確認したい場合:

```bash
openclaw dashboard --no-open
```

補足:

- `openclaw dashboard` は現在のトークンで Control UI を開く
- 事前に Gateway が起動している必要がある

手順:

1. WebDashboard にアクセスする
2. OpenClaw の入力欄に場所検索の依頼を入れる
3. 返答内容に Google Maps の検索 URL が含まれることを確認する

確認例:

- 東京駅を Google Maps で開きたい
- 新宿駅南口の地図を出して

確認ポイント:

- TUI と同じ意図で Skill が呼ばれること
- JSON や内部情報ではなく、利用しやすい形で結果が返ること
- ブラウザ上でリンクを開けること

## 4. Discord からのテスト

Discord 連携の設定は完了済みである前提で、実際のチャット経由でも同じ結果になることを確認します。

手順:

1. Discord の OpenClaw 連携チャンネルを開く
2. 場所検索の依頼を送る
3. 返答に Google Maps の URL が含まれることを確認する

確認例:

- 東京駅を Google Maps で開きたい
- らりるれろを Google Maps で検索して

確認ポイント:

- Discord 上でも応答が冗長になりすぎないこと
- 不自然な語でも検索 URL が生成されること
- 空入力や曖昧な入力時は、再入力を促すこと

## 検証時の見方

この Skill は「地名を確定する」ものではなく、「Google Maps の検索 URL を返す」ものです。
そのため検証では、検索候補の正確性ではなく、次の点を主に見ます。

- 入力文字列がそのまま検索語として扱われること
- Google Maps の URL が正しい形式で組み立てられていること
- 失敗時に JSON または短い説明で再入力を促せること
