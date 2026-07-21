from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .io_utils import load_findings, write_json, write_text
from .planner import render_plan
from .queries import build_search_tasks
from .report import render_report


def _aliases(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jent-radar",
        description=(
            "Generate public-source search plans and evidence-tiered reports "
            "for Japanese entertainment resources."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Create an artist watchlist JSON file."
    )
    init_parser.add_argument("--artist", required=True)
    init_parser.add_argument("--aliases", default="")
    init_parser.add_argument("--window", default="")
    init_parser.add_argument(
        "--output", required=True, help="Output JSON file, e.g. watchlists/artist.json"
    )

    plan_parser = subparsers.add_parser(
        "plan", help="Generate a Markdown search plan."
    )
    plan_parser.add_argument("--artist", required=True)
    plan_parser.add_argument("--aliases", default="")
    plan_parser.add_argument("--window", default="")
    plan_parser.add_argument("--output", required=True)

    report_parser = subparsers.add_parser(
        "report", help="Generate an evidence-tiered Markdown report."
    )
    report_parser.add_argument("--artist", required=True)
    report_parser.add_argument("--window", default="")
    report_parser.add_argument("--findings", required=True)
    report_parser.add_argument("--output", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            payload = {
                "artist": args.artist,
                "aliases": _aliases(args.aliases),
                "window": args.window,
                "focus": [
                    "television_drama",
                    "film",
                    "streaming",
                    "stage",
                    "mc",
                    "commercial",
                    "public_rumor_spillover",
                ],
                "privacy": {
                    "public_sources_only": True,
                    "no_private_accounts": True,
                    "no_private_location_tracking": True,
                },
            }
            write_json(args.output, payload)
            print(f"Created watchlist: {Path(args.output)}")
            return 0

        if args.command == "plan":
            aliases = _aliases(args.aliases)
            tasks = build_search_tasks(args.artist, aliases, args.window)
            markdown = render_plan(args.artist, aliases, args.window, tasks)
            write_text(args.output, markdown)
            print(f"Created search plan: {Path(args.output)}")
            return 0

        if args.command == "report":
            findings = load_findings(args.findings)
            markdown = render_report(args.artist, args.window, findings)
            write_text(args.output, markdown)
            print(f"Created report: {Path(args.output)}")
            return 0

    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
