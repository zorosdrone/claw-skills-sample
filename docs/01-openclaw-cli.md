# OpenClaw CLI 最小実行例

このドキュメントは、`openclaw agent` をコマンドラインから最小構成で実行するための手順をまとめたものです。

## 1. 先に押さえる必須条件

`openclaw agent` は、メッセージ本文だけを位置引数で渡しても動きません。

最低限、次の 2 種類が必要です。

1. メッセージ本文
2. どのセッションまたはエージェントへ送るか

必須になる代表オプション:

- `-m` または `--message`
- `--agent` または `--session-id` または `--to`

## 2. 最小成功例

### 2-1. `--agent` を使う

```bash
openclaw agent --agent main --thinking low -m "東京の明日の天気は？"
```

この形は、TUI などで `agent main` を使っている場合に分かりやすい実行方法です。

### 2-2. `--session-id` を使う

```bash
openclaw agent --session-id main --thinking low -m "東京の明日の天気は？"
```

同じ `main` セッションへ明示的に送る例です。

### 2-3. JSON で受ける

```bash
openclaw agent --agent main --thinking minimal -m "東京の明日の天気は？" --json
```

CLI の疎通確認では、まずこの形で試すとエラー内容を追いやすくなります。

## 3. よくある失敗例

### 3-1. `--message` を付けていない

失敗例:

```bash
openclaw agent --thinking low "東京の明日の天気は？"
```

この場合は、次のようなエラーになります。

```text
error: required option '-m, --message <text>' not specified
```

修正例:

```bash
openclaw agent --thinking low -m "東京の明日の天気は？"
```

ただし、これだけではまだ不十分です。次の失敗に続きます。

### 3-2. セッションやエージェントを指定していない

失敗例:

```bash
openclaw agent --thinking low -m "東京の明日の天気は？"
```

この場合は、次のようなエラーになります。

```text
Error: Pass --to <E.164>, --session-id, or --agent to choose a session
```

修正例:

```bash
openclaw agent --agent main --thinking low -m "東京の明日の天気は？"
```

または:

```bash
openclaw agent --session-id main --thinking low -m "東京の明日の天気は？"
```

## 4. TUI で 400 が出たときの切り分け

TUI で `400 {"message":"","code":"invalid_request_body"}` が出た場合、まずは TUI 固有の問題か、CLI 全体の指定ミスかを切り分けます。

最初に試すコマンド:

```bash
openclaw agent --agent main --thinking low -m "東京の明日の天気は？"
```

このコマンドが通る場合:
- モデルへの基本経路は生きている
- TUI 側のセッション状態や送信形式を疑う

このコマンドも失敗する場合:
- 引数不足
- セッション指定不足
- CLI 側の設定不整合

の順で疑います。

### 4-1. TUI 側での確認順

TUI でエラーが出た場合は、次の順で切り分けると早いです。

1. まず TUI と同じ内容を CLI で投げる
2. CLI で通るなら、TUI セッションを作り直す
3. それでも TUI だけ落ちるなら、TUI の送信経路を疑う

最初に使う確認コマンド:

```bash
openclaw agent --agent main --thinking low -m "東京の明日の天気は？"
```

このコマンドが成功した場合の判断:
- モデル自体は応答できている
- `--message` と送信先指定の不足ではない
- TUI 固有のセッション状態か送信形式を疑う

### 4-2. TUI 再確認の具体例

1 回 CLI で成功を確認したあと、TUI では同じ意味の短い入力で再試行します。

例:

```text
東京の明日の天気は？
```

ここで再び `400 {"message":"","code":"invalid_request_body"}` が出るなら、ユーザー入力の内容より TUI 側のリクエスト生成を疑うべきです。

### 4-3. 実務上の回避策

TUI 側が不安定な間は、まず CLI で疎通確認を進めます。

通常会話の確認:

```bash
openclaw agent --agent main --thinking low -m "東京の明日の天気は？"
```

Skill 実行確認:

```bash
openclaw agent --agent main --thinking low -m "/skill 02-con-sitl trigkeys5-wsl に ping が通るか確認して。JSONをそのまま返して。"
```

TUI は、CLI で基本経路が通ることを確認してから戻る方が無駄が少ないです。

## 5. Skill 呼び出しの確認例

Skill 実行を CLI から確かめたい場合は、メッセージ本文に Skill 指定を含めます。

例:

```bash
openclaw agent --agent main --thinking low -m "/skill 02-con-sitl trigkeys5-wsl に ping が通るか確認して。JSONをそのまま返して。"
```

この形なら、通常会話と Skill 実行の両方を同じ CLI から試せます。

## 6. まず覚える形

最初は次の 1 行だけ覚えておけば十分です。

```bash
openclaw agent --agent main --thinking low -m "メッセージ本文"
```

必要になったら、`--session-id main` や `--json` を追加します。