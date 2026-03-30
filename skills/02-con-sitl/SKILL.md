---
name: 02-con-sitl
description: 別PCで動く ArduPilot SITL ホストの到達性を確認する Skill。TailScale 越しに ping 疎通を確認したい依頼では、この Skill を優先して execution_id, host, reachable を返す。
---

# ArduPilot SITL ホストの到達性を確認する Skill

利用場面:
- `SITL 用PCに ping が通るか確認したい`
- `WSL2 上の ArduPilot SITL ホストが生きているか見たい`
- `TailScale 越しに sitl-pc へ疎通確認して`

この Skill は、別PC の WSL2 上で動いている ArduPilot SITL 用ホストに対して ping を実行し、到達できるかを JSON で返す。
『SITL の状態を見たい』『SITL ホストに届くか確認したい』『TailScale 越しに疎通確認したい』のような依頼では、この Skill を優先して使う。

この種の依頼では、この Skill を優先して使う:
- SITL ホストに ping が通るか見たい
- 別PC の WSL2 に疎通確認したい
- TailScale 名や IP で到達確認したい

疎通確認だけで十分な依頼では、一般知識だけで自然文回答せず、この Skill を使って `execution_id`, `host`, `reachable` を返す。

## Safety Defaults
- 実際の確認は `ping` コマンドだけで行う
- 今回の最小構成ではドローンの詳細テレメトリまでは確認しない
- ホスト名または IP が無い場合は再入力を求める
- 外部 API 呼び出しや追加の依存パッケージ導入は行わない
- 到達不可でも、確認結果として JSON を返す

## 実行コマンド

基本形:

```bash
python3 skills/02-con-sitl/scripts/ping.py --host sitl-host
```

位置引数でも実行できる:

```bash
python3 skills/02-con-sitl/scripts/ping.py sitl-host
```

## Expected Output

返却は JSON とする。
スクリプトの標準出力 JSON をそのまま返し、自然文へ言い換えない。
前置き、要約、完了メッセージを追加しない。

成功例:

```json
{
  "ok": true,
  "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f",
  "host": "sitl-host",
  "reachable": true,
  "returncode": 0,
  "summary": "1 packets transmitted, 1 received, 0% packet loss"
}
```

到達不可の例:

```json
{
  "ok": true,
  "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f",
  "host": "sitl-host",
  "reachable": false,
  "returncode": 1,
  "summary": "1 packets transmitted, 0 received, 100% packet loss"
}
```

エラー例:

```json
{
  "ok": false,
  "execution_id": "9f7a6b6a99ab4bf0bde2f835428b0e2f",
  "error": "SITL host is required",
  "hint": "例: python3 skills/02-con-sitl/scripts/ping.py --host sitl-host"
}
```

## Response Style
- 成功時はスクリプトの標準出力 JSON をそのまま返す
- JSON の前後に自然文を付けない
- Markdown 整形やコードブロックで包まない
- `execution_id`, `host`, `reachable` を含む JSON を返す
- エラー時もエラー JSON をそのまま返す

## Notes
- 前提は OpenClaw 側と SITL 側の双方で TailScale が利用可能であること
- `host` には TailScale 名または疎通可能な IP を渡す
- 必要な依存関係は Python 標準ライブラリと OS 標準の `ping` コマンドのみ
- 実行ログは標準エラーに JSON Lines で出力する
- 既定の保存先は `~/.openclaw/workspace/logs/skills/02-con-sitl.jsonl`
- `execution_id` は標準出力 JSON とログの両方に含まれ、実行確認の突合に使える
- 実処理は `scripts/ping.py` が担当する