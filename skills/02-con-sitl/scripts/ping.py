#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid


SKILL_NAME = "02-con-sitl"


def resolve_log_file_path(explicit_path: str | None) -> Path | None:
    if explicit_path:
        return Path(explicit_path).expanduser()

    workspace_dir = os.environ.get("OPENCLAW_WORKSPACE_DIR")
    if workspace_dir:
        return Path(workspace_dir).expanduser() / "logs" / "skills" / f"{SKILL_NAME}.jsonl"

    home_dir = os.environ.get("HOME")
    if not home_dir:
        return None

    return Path(home_dir).expanduser() / ".openclaw" / "workspace" / "logs" / "skills" / f"{SKILL_NAME}.jsonl"


class EventLogger:
    def __init__(self, log_file_path: Path | None, execution_id: str) -> None:
        self.log_file_path = log_file_path
        self.execution_id = execution_id

    def emit(self, stage: str, **fields: object) -> None:
        log_record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "execution_id": self.execution_id,
            "stage": stage,
        }
        if fields:
            log_record.update(fields)

        serialized = json.dumps(log_record, ensure_ascii=False)
        print(serialized, file=sys.stderr)

        if not self.log_file_path:
            return

        try:
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_file_path.open("a", encoding="utf-8") as log_file:
                log_file.write(serialized + "\n")
        except OSError as exc:
            print(
                json.dumps(
                    {
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "execution_id": self.execution_id,
                        "stage": "log_write_error",
                        "error": str(exc),
                        "log_file": str(self.log_file_path),
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the ArduPilot SITL host is reachable via ping"
    )
    parser.add_argument(
        "host_terms",
        nargs="*",
        help="SITL host name or IP as positional text, for example: sitl-host",
    )
    parser.add_argument(
        "--host",
        help="SITL host name or IP to check with ping",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of ping packets to send. Default: 1",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=2,
        help="Ping timeout in seconds. Default: 2",
    )
    parser.add_argument(
        "--log-file",
        help=(
            "Append execution logs as JSON Lines to this file. "
            "Default: ~/.openclaw/workspace/logs/skills/02-con-sitl.jsonl"
        ),
    )
    parser.add_argument(
        "--no-file-log",
        action="store_true",
        help="Disable file logging and only emit logs to stderr",
    )
    return parser.parse_args()


def resolve_host(args: argparse.Namespace) -> str:
    if args.host and args.host.strip():
        return args.host.strip()

    positional_host = " ".join(args.host_terms).strip()
    if positional_host:
        return positional_host

    raise ValueError("SITL host is required")


def validate_args(args: argparse.Namespace) -> None:
    if args.count < 1:
        raise ValueError("count must be greater than or equal to 1")
    if args.timeout_seconds < 1:
        raise ValueError("timeout-seconds must be greater than or equal to 1")


def last_non_empty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def run_ping(host: str, count: int, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    command = ["ping", "-c", str(count), "-W", str(timeout_seconds), host]
    return subprocess.run(command, capture_output=True, text=True, check=False)


def main() -> int:
    execution_id = uuid.uuid4().hex
    log_file_path: Path | None = None

    try:
        args = parse_args()
        validate_args(args)
        log_file_path = None if args.no_file_log else resolve_log_file_path(args.log_file)
        logger = EventLogger(log_file_path=log_file_path, execution_id=execution_id)
        logger.emit("start", argv=sys.argv[1:], log_file=str(log_file_path) if log_file_path else None)
        logger.emit(
            "args_parsed",
            has_host=bool(args.host),
            host_terms=args.host_terms,
            count=args.count,
            timeout_seconds=args.timeout_seconds,
        )

        host = resolve_host(args)
        logger.emit("host_resolved", host=host)

        result = run_ping(host=host, count=args.count, timeout_seconds=args.timeout_seconds)
        summary = last_non_empty_line(result.stdout) or last_non_empty_line(result.stderr)
        reachable = result.returncode == 0

        output = {
            "ok": True,
            "execution_id": execution_id,
            "host": host,
            "reachable": reachable,
            "returncode": result.returncode,
            "summary": summary,
        }
        logger.emit(
            "success",
            host=host,
            reachable=reachable,
            returncode=result.returncode,
            summary=summary,
        )
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except FileNotFoundError as exc:
        logger = EventLogger(log_file_path=log_file_path or resolve_log_file_path(None), execution_id=execution_id)
        logger.emit("error", error=str(exc))
        print(
            json.dumps(
                {
                    "ok": False,
                    "execution_id": execution_id,
                    "error": "ping command is not available",
                    "hint": "OS 標準の ping コマンドが使える環境で実行してください",
                },
                ensure_ascii=False,
            )
        )
        return 1
    except Exception as exc:
        logger = EventLogger(log_file_path=log_file_path or resolve_log_file_path(None), execution_id=execution_id)
        logger.emit("error", error=str(exc))
        print(
            json.dumps(
                {
                    "ok": False,
                    "execution_id": execution_id,
                    "error": str(exc),
                    "hint": "例: python3 skills/02-con-sitl/scripts/ping.py --host sitl-host",
                },
                ensure_ascii=False,
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())