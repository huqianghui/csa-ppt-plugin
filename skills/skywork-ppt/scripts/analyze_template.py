#!/usr/bin/env python3
"""Inspect a local PPTX template and print layout information."""

import argparse
import json
import sys

from ppt_core import analyze_template


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a local PPTX template")
    parser.add_argument("template", help="Path to the template PPTX")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    try:
        report = analyze_template(args.template)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"Template: {report['template_file']}")
            print(f"Slides: {report['slide_count']}")
            print(f"Size: {report['slide_width_inches']}in x {report['slide_height_inches']}in")
            print("Layouts:")
            for layout in report["layouts"]:
                print(f"  - [{layout['index']}] {layout['name']} ({layout['placeholders']} placeholders)")
            print("Sample slide titles:")
            for slide in report["sample_titles"][:8]:
                print(f"  - Slide {slide['slide']}: {slide['title']}")
        print("RESULT: success")
    except Exception as exc:
        print("RESULT: error")
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()