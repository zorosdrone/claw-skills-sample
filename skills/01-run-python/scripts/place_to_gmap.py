#!/usr/bin/env python3
import argparse
import json
import sys
from urllib.parse import quote_plus


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
    return parser.parse_args()


def resolve_query(args: argparse.Namespace) -> str:
    if args.query and args.query.strip():
        return args.query.strip()

    positional_query = " ".join(args.terms).strip()
    if positional_query:
        return positional_query

    raise ValueError("place name is required")


def main() -> int:
    try:
        args = parse_args()
        query = resolve_query(args)
        output = {
            "ok": True,
            "query": query,
            "map_url": build_map_url(query),
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "hint": "例: python3 skills/01-run-python/scripts/place_to_gmap.py --query '東京駅'",
                },
                ensure_ascii=False,
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())