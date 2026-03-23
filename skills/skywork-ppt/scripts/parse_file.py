#!/usr/bin/env python3
"""Parse local reference files into plain text for the PPT workflow."""

import argparse
import csv
import json
import os
import re
import sys
import zipfile
from html import unescape
from xml.etree import ElementTree

from config import SUPPORTED_TEXT_EXTENSIONS
from ppt_core import extract_presentation_text


def _read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def _read_csv_file(file_path: str) -> str:
    rows = []
    with open(file_path, "r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            rows.append(", ".join(cell.strip() for cell in row))
    return "\n".join(rows)


def _read_json_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _strip_html(text: str) -> str:
    return unescape(re.sub(r"<[^>]+>", " ", text))


def _read_docx_file(file_path: str) -> str:
    with zipfile.ZipFile(file_path) as archive:
        xml_bytes = archive.read("word/document.xml")
    root = ElementTree.fromstring(xml_bytes)
    paragraphs = []
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for paragraph in root.findall(".//w:p", namespace):
        texts = [node.text for node in paragraph.findall(".//w:t", namespace) if node.text]
        line = "".join(texts).strip()
        if line:
            paragraphs.append(line)
    return "\n".join(paragraphs)


def parse_local_file(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_TEXT_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext in {".txt", ".md"}:
        text = _read_text_file(file_path)
    elif ext == ".csv":
        text = _read_csv_file(file_path)
    elif ext == ".json":
        text = _read_json_file(file_path)
    elif ext in {".html", ".htm"}:
        text = _strip_html(_read_text_file(file_path))
    elif ext == ".docx":
        text = _read_docx_file(file_path)
    elif ext == ".pptx":
        text = extract_presentation_text(file_path)["text"]
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return {
        "filename": os.path.basename(file_path),
        "file_type": ext.lstrip("."),
        "path": os.path.abspath(file_path),
        "text": text,
        "text_length": len(text),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a local reference file into plain text")
    parser.add_argument("file", help="Path to the file to parse")
    parser.add_argument("--output", "-o", default="", help="Save parsed text to this file")
    parser.add_argument("--json", action="store_true", help="Print JSON payload")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"RESULT: error")
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        result = parse_local_file(args.file)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(result["text"])
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            preview = result["text"][:1000]
            print(preview)
            if len(result["text"]) > 1000:
                print(f"\n... ({len(result['text']) - 1000} more characters)")
        machine = dict(result)
        machine.pop("text")
        print(f"PARSED_FILE: {json.dumps(machine, ensure_ascii=False)}")
    except Exception as exc:
        print("RESULT: error")
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
