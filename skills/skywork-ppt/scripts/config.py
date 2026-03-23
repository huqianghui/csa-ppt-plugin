#!/usr/bin/env python3
"""Configuration for the local-first PPT skill."""

import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
DEFAULT_OUTPUT_DIR = Path(os.environ.get("PPT_OUTPUT_DIR", str(SKILL_ROOT / "outputs")))
DEFAULT_STAGING_DIR = Path(os.environ.get("PPT_STAGING_DIR", str(SKILL_ROOT / ".staging")))
DEFAULT_LANGUAGE = os.environ.get("PPT_DEFAULT_LANGUAGE", "Chinese")
DEFAULT_MAX_SLIDES = int(os.environ.get("PPT_DEFAULT_MAX_SLIDES", "8"))

DEFAULT_THEME = {
	"accent": os.environ.get("PPT_THEME_ACCENT", "#0F6CBD"),
	"background": os.environ.get("PPT_THEME_BACKGROUND", "#FFFFFF"),
	"text": os.environ.get("PPT_THEME_TEXT", "#1F1F1F"),
	"muted": os.environ.get("PPT_THEME_MUTED", "#5B5B5B"),
}

SUPPORTED_TEXT_EXTENSIONS = {
	".txt",
	".md",
	".json",
	".csv",
	".html",
	".htm",
	".docx",
	".pptx",
}


def ensure_runtime_dirs() -> None:
	DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	DEFAULT_STAGING_DIR.mkdir(parents=True, exist_ok=True)


def resolve_output_path(output_path: str) -> Path:
	ensure_runtime_dirs()
	output = Path(output_path).expanduser()
	if not output.is_absolute():
		output = DEFAULT_OUTPUT_DIR / output
	output.parent.mkdir(parents=True, exist_ok=True)
	return output


def resolve_staging_dir(path: str = "") -> Path:
	ensure_runtime_dirs()
	staging_dir = Path(path).expanduser() if path else DEFAULT_STAGING_DIR
	if not staging_dir.is_absolute():
		staging_dir = DEFAULT_STAGING_DIR / staging_dir
	staging_dir.mkdir(parents=True, exist_ok=True)
	return staging_dir


def default_slide_theme() -> dict:
	return dict(DEFAULT_THEME)


def local_backend_description() -> str:
	return "Local Claude Code PPT workflow with external search handled by configured MCP tools."
