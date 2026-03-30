#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import uuid
from urllib.parse import quote_plus


SKILL_NAME = "01-run-python"


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


def build_map_url(query: str) -> str:
    encoded_query = quote_plus(query)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_query}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a place name into a Google Maps search URL"
    )
    parser.add_argument(
        "terms",
        nargs="*",
        help="Place name as positional text, for example: 東京駅",
    )
    parser.add_argument(
        "--query",
        help="Place name or search text to convert into a Google Maps URL",
    )
    parser.add_argument(
        "--log-file",
        help=(
            "Append execution logs as JSON Lines to this file. "
            "Default: ~/.openclaw/workspace/logs/skills/01-run-python.jsonl"
        ),
    )
    parser.add_argument(
        "--no-file-log",
        action="store_true",
        help="Disable file logging and only emit logs to stderr",
    )
    return parser.parse_args()


def resolve_query(args: argparse.Namespace) -> str:
    if args.query and args.query.strip():
        return args.query.strip()

    positional_query = " ".join(args.terms).strip()
    if positional_query:
        return positional_query

    raise ValueError("place name is required")


def main() -> int:
    execution_id = uuid.uuid4().hex
    try:
        args = parse_args()
        log_file_path = None if args.no_file_log else resolve_log_file_path(args.log_file)
        logger = EventLogger(log_file_path=log_file_path, execution_id=execution_id)
        logger.emit("start", argv=sys.argv[1:], log_file=str(log_file_path) if log_file_path else None)
        logger.emit("args_parsed", has_query=bool(args.query), terms=args.terms)
        query = resolve_query(args)
        logger.emit("query_resolved", query=query)
        output = {
            "ok": True,
            "execution_id": execution_id,
            "query": query,
            "map_url": build_map_url(query),
        }
        logger.emit("success", query=query, map_url=output["map_url"])
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except Exception as exc:
        logger = EventLogger(log_file_path=resolve_log_file_path(None), execution_id=execution_id)
        logger.emit("error", error=str(exc))
        print(
            json.dumps(
                {
                    "ok": False,
                    "execution_id": execution_id,
                    "error": str(exc),
                    "hint": "例: python3 skills/01-run-python/scripts/place_to_gmap.py --query '東京駅'",
                },
                ensure_ascii=False,
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())