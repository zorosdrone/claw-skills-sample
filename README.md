# claw-skills-sample

OpenClaw の Skill 学習用プロジェクトです。
目標は、日本語で使える Skill を最小構成で作成し、配置、認識確認、テストまで一通り試せる状態にすることです。

## このリポジトリ内の文書の役割

- この README: リポジトリ全体の概要、共通の配置方法、認識確認、テスト手順
- [skills/01-run-python/README.md](skills/01-run-python/README.md): `01-run-python` サンプルの概要、入出力、実行例
- [skills/01-run-python/SKILL.md](skills/01-run-python/SKILL.md): OpenClaw が実行時に参照する Skill 定義本体
- [docs/01-run-python.md](docs/01-run-python.md): `01-run-python` を生成するための TUI プロンプト例と設計メモ

## サンプル一覧

- [skills/01-run-python/README.md](skills/01-run-python/README.md): 地名や施設名から Google Maps の検索 URL を返す最小 Skill サンプル

参考プロジェクト:

- https://github.com/zorosdrone/claw-sitl-ops

前提:

- XServer 無料VPS 上で OpenClaw を常駐
- 最新版 OpenClaw を利用
- Tailscale 稼働済み
- Discord 連携も想定
- ArdupilotSITL は Windows PC の WSL で動かす
- Windows PC / WSL 側にも Tailscale 導入済み
- このプロジェクトは OpenClaw が動いているマシンで開発されている

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
- OpenClaw CLI で参照する Skill 名は `SKILL.md` の frontmatter の `name` を使う
- フォルダ名と `name` は一致させると管理しやすい

Workspace の skills へ上書き反映するには:

```bash
scripts/sync_skill_to_workspace.sh 01-run-python
```

このスクリプトは、リポジトリ側の `skills/<skill_name>/SKILL.md` と `skills/<skill_name>/scripts/` を `~/.openclaw/workspace/skills/<skill_name>/` に上書きコピーします。

リポジトリ側で `SKILL.md` や `scripts/` を変更した後は、テスト前に必ずこの同期を再実行します。

同期後にログファイルを確認する例:

```bash
tail -n 20 ~/.openclaw/workspace/logs/skills/01-run-python.jsonl
```

## Skill 配置後の認識確認

1. 利用可能な Skill 一覧を表示する

```bash
openclaw skills list
```

2. 対象 Skill の詳細を確認する

```bash
openclaw skills info 01-run-python
```

3. Skill の readiness を確認する

```bash
openclaw skills check
```

必要なら詳細表示:

```bash
openclaw skills check --verbose
```

確認ポイント:

- `01-run-python` が一覧に表示されること
- `skills info` で `SKILL.md` の情報が取得できること
- `skills check` で ready として扱われること

表示されない場合の確認項目:

- ディレクトリが `skills/01-run-python/` になっているか
- `SKILL.md` がその直下にあるか
- `SKILL.md` の frontmatter が壊れていないか
- `name` や説明の記述に不整合がないか

## 共通テスト手順

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

### 1. コマンドラインからのテスト

まずはスクリプト単体で正しい JSON が返ることを確認します。
サンプル固有の入出力は [skills/01-run-python/README.md](skills/01-run-python/README.md) を参照してください。

```bash
python3 skills/01-run-python/scripts/place_to_gmap.py --query "東京駅"
```

確認観点:

- `ok`, `query`, `map_url` の 3 つが返ること
- `query` が入力値と一致すること
- `map_url` が Google Maps 検索 URL 形式になっていること
- 仕様にない `label`, `center`, `zoom` などを返していないこと

補足:

- このサンプルの動作確認は「Google Maps で期待した候補が開くか」ではなく、「スクリプトが決めた JSON 契約どおりに返すか」を見る
- URL が開けるだけでは、Skill の実装どおりに動いた確認としては不十分
- 実行ログは `~/.openclaw/workspace/logs/skills/01-run-python.jsonl` に追記される
- 運用中に確認するときは `tail -f ~/.openclaw/workspace/logs/skills/01-run-python.jsonl` を使う

### 2. TUI からのテスト

```bash
openclaw tui
```

確認ポイント:

- `01-run-python` の Skill が選ばれること
- URL だけ、または簡潔な説明つきで返答されること

### 3. WebDashboard からのテスト

```bash
openclaw dashboard
```

URL だけ確認したい場合:

```bash
openclaw dashboard --no-open
```

確認ポイント:

- TUI と同じ意図で Skill が呼ばれること
- ブラウザ上でリンクを開けること
- チャット応答が補足情報を付ける場合でも、元の Skill 仕様は `query` と `map_url` を返すだけであることを意識すること

Web の Chat に入力する例:

```text
/skill 01-run-python 東京駅
```

または:

```text
/skill 01-run-python 東京をGoogleマップで見たい
```

確認できたと言える条件:

- `01-run-python` を明示して呼んでいること
- 返答の中に `query` と `map_url` が含まれること
- `map_url` が `https://www.google.com/maps/search/?api=1&query=...` の形式になっていること
- `query` が入力した地名に対応していること

「Skill と Script が起動した」とは言い切れない例:

- 単に Google Maps のリンクだけが自然文で返る
- `label`, `center`, `zoom` など仕様外の情報だけが目立つ
- `query` と `map_url` が見えず、チャットが要約だけ返している

判定を明確にしたい場合の入力例:

```text
/skill 01-run-python 東京駅を検索して。生のJSONとして query と map_url を返して。
```

この入力を使う理由:

- Skill 名を固定できる
- JSON の確認対象を `query` と `map_url` に絞れる
- UI 側の補足整形が入っても、仕様どおりの返答か見分けやすい

### 4. Discord からのテスト

Discord 連携の設定は完了済みである前提です。

確認ポイント:

- Discord 上でも応答が冗長になりすぎないこと
- 空入力や曖昧な入力時は再入力を促せること

## 補足

この Skill は「地名を確定する」ものではなく、「Google Maps の検索 URL を返す」ものです。
サンプルの具体的な用途と出力例は [skills/01-run-python/README.md](skills/01-run-python/README.md)、生成プロンプト例は [docs/01-run-python.md](docs/01-run-python.md) を参照してください。

特に WebDashboard やチャット経由の返答は、UI 側や会話応答で補足整形されることがあります。
そのため、厳密な動作確認はスクリプトの生出力 JSON を基準に行うのが安全です。
