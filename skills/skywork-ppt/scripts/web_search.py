#!/usr/bin/env python3
"""Assemble local search notes into a single reference markdown file.

Actual web searching should be done through the user's configured MCP server tools.
This script only normalizes the collected notes into one reference file for PPT generation.
"""

import argparse
import json
import os
import sys


def build_reference(title: str, queries, input_files) -> str:
    sections = [f"# {title}"]
    if queries:
        sections.append("## Queries")
        for query in queries:
            sections.append(f"- {query}")

    sections.append("## Source Notes")
    for path in input_files:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read().strip()
        sections.append(f"### {os.path.basename(path)}")
        sections.append(content or "(empty)")
    return "\n\n".join(sections).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge MCP search notes into a reference markdown file")
    parser.add_argument("inputs", nargs="+", help="Local text or markdown files containing search notes")
    parser.add_argument("--title", default="Reference Report", help="Reference document title")
    parser.add_argument("--query", action="append", default=[], help="Original search query, repeatable")
    parser.add_argument("-o", "--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    try:
        reference = build_reference(args.title, args.query, args.inputs)
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(reference)
        print("RESULT: success")
        print(f"OUTPUT_FILE: {os.path.abspath(args.output)}")
        print(f"INPUT_COUNT: {len(args.inputs)}")
        print(f"QUERIES: {json.dumps(args.query, ensure_ascii=False)}")
    except Exception as exc:
        print("RESULT: error")
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
