#!/usr/bin/env python3
"""Local PPT generation entrypoint for Claude Code workflows."""

import argparse
import json
import sys

from config import DEFAULT_LANGUAGE, DEFAULT_MAX_SLIDES, resolve_output_path
from parse_file import parse_local_file
from ppt_core import apply_edit_plan, build_basic_outline, load_json_file, render_presentation


def _load_json_payload(inline_payload: str, file_path: str, label: str):
    if inline_payload and file_path:
        raise ValueError(f"Use either inline {label} JSON or --{label}-file, not both")
    if inline_payload:
        return json.loads(inline_payload)
    if file_path:
        return load_json_file(file_path)
    return None


def _read_reference(args) -> str:
    parts = []
    reference = args.reference.strip()
    if reference:
        parts.append(reference)
    if args.reference_file:
        with open(args.reference_file, "r", encoding="utf-8") as handle:
            file_reference = handle.read().strip()
        if file_reference:
            parts.append(file_reference)

    for path in args.reference_path or []:
        parsed = parse_local_file(path)
        text = parsed["text"].strip()
        if not text:
            continue
        parts.append(f"# Source: {parsed['filename']}\n\n{text}")

    return "\n\n".join(parts).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or edit PPTX files locally")
    parser.add_argument("query", nargs="?", default="", help="User query or deck title")
    parser.add_argument("--mode", choices=["auto", "generate", "template", "edit"], default="auto")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help="Deck language label")
    parser.add_argument("--reference", default="", help="Inline reference text")
    parser.add_argument("--reference-file", default="", help="Path to a local reference markdown/text file")
    parser.add_argument("--reference-path", action="append", default=[], help="Local file path to parse and merge into reference text, repeatable")
    parser.add_argument("--outline", default="", help="Inline outline JSON payload")
    parser.add_argument("--outline-file", default="", help="Path to an outline JSON file")
    parser.add_argument("--template-file", default="", help="Path to a local .pptx template file")
    parser.add_argument("--pptx-file", default="", help="Existing .pptx file to edit")
    parser.add_argument("--edit-plan", default="", help="Inline edit plan JSON payload")
    parser.add_argument("--edit-plan-file", default="", help="JSON file describing local edits")
    parser.add_argument("--max-slides", type=int, default=DEFAULT_MAX_SLIDES, help="Maximum slides for auto outline generation")
    parser.add_argument("-o", "--output", default="output.pptx", help="Output .pptx path")
    args = parser.parse_args()

    output = resolve_output_path(args.output)
    mode = args.mode
    if mode == "auto":
        if args.edit_plan_file or args.pptx_file:
            mode = "edit"
        elif args.template_file:
            mode = "template"
        else:
            mode = "generate"

    print(f"[PHASE] Running local PPT workflow in {mode} mode", flush=True)

    try:
        if mode == "edit":
            if not args.pptx_file:
                raise ValueError("Edit mode requires --pptx-file")
            print("[PHASE] Loading edit plan", flush=True)
            edit_plan = _load_json_payload(args.edit_plan, args.edit_plan_file, "edit-plan")
            if not edit_plan:
                raise ValueError("Edit mode requires --edit-plan or --edit-plan-file")
            result = apply_edit_plan(args.pptx_file, str(output), edit_plan)
            print("[PHASE] Applied edit plan", flush=True)
            print(f"RESULT: success")
            print(f"MODE: edit")
            print(f"OUTPUT_FILE: {result['output_file']}")
            print(f"SLIDE_COUNT: {result['slide_count']}")
            print(f"SUMMARY: {json.dumps(result['summary'], ensure_ascii=False)}")
            return

        reference_text = _read_reference(args)
        print("[PHASE] Building outline", flush=True)
        outline = _load_json_payload(args.outline, args.outline_file, "outline")
        if outline is None:
            outline = build_basic_outline(args.query, reference_text, args.language, max_slides=args.max_slides)

        print("[PHASE] Rendering slides", flush=True)
        result = render_presentation(outline, str(output), template_file=args.template_file)
        print("[PHASE] Saved presentation", flush=True)
        print("RESULT: success")
        print(f"MODE: {mode}")
        print(f"OUTPUT_FILE: {result['output_file']}")
        print(f"SLIDE_COUNT: {result['slide_count']}")
        print(f"SLIDE_TITLES: {json.dumps(result['slide_titles'], ensure_ascii=False)}")
    except Exception as exc:
        print(f"RESULT: error")
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
