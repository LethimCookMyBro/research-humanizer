#!/usr/bin/env python3
"""Read-only, heuristic style checks for UTF-8 Markdown and plain text.

This is not a Markdown compiler or a scientific, plagiarism, anonymity, or
layout validator. Review every finding. Exact quotations need human review.
Protected syntax supported here includes YAML frontmatter, fenced code,
inline code, URLs, common inline/display math, and reference sections.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

CONTRACTIONS = re.compile(
    r"\b(?:[a-z]+n['’]t|(?:i|you|we|they|he|she|it|that|there|what|who|how|where|when|why)"
    r"['’](?:m|re|ve|ll|d|s)|let['’]s)\b", re.IGNORECASE
)
PLACEHOLDERS = re.compile(
    r"\[(?:SOURCE REQUIRED|RESULT UNVERIFIED|AUTHOR DECISION|CITATION NEEDED|TBD|TODO)\]"
    r"|\{\{[^}\n]+\}\}", re.IGNORECASE
)
REFERENCE_NAMES = {"references", "bibliography", "เอกสารอ้างอิง", "บรรณานุกรม"}


def mask_inline(text: str) -> str:
    """Mask common technical syntax while retaining Markdown link labels."""
    text = re.sub(r"(`+).*?\1", " ", text)
    text = re.sub(r"\\\(.*?\\\)", " ", text)
    text = re.sub(r"\$\$.*?\$\$", " ", text)
    text = re.sub(r"(?<![\\$])\$(?!\$).*?(?<!\\)\$", " ", text)
    text = re.sub(r"\\\[.*?\\\]", " ", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"(?:https?://|doi:)\S+", " ", text, flags=re.IGNORECASE)
    return text


def lint_text(text: str) -> list[dict[str, Any]]:
    """Return possible style defects without altering the manuscript."""
    findings: list[dict[str, Any]] = []
    in_yaml = False
    fence_char: str | None = None
    fence_len = 0
    display_end: str | None = None
    reference_level: int | None = None

    def add(number: int, rule: str, message: str, original: str) -> None:
        findings.append({"line": number, "rule": rule, "message": message,
                         "excerpt": original.strip()[:180]})

    for number, original in enumerate(text.splitlines(), start=1):
        line = original.lstrip("\ufeff") if number == 1 else original
        stripped = line.strip()
        if number == 1 and stripped == "---":
            in_yaml = True
            continue
        if in_yaml:
            if stripped in {"---", "..."}:
                in_yaml = False
            continue

        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            continue

        if display_end is not None:
            if display_end in line:
                line = line.split(display_end, 1)[1]
                display_end = None
            else:
                continue
        # Protect multi-line display equations. Same-line forms are masked later.
        for opening, closing in (("$$", "$$"), (r"\[", r"\]")):
            if opening in line:
                prefix, suffix = line.split(opening, 1)
                if closing not in suffix:
                    line = prefix
                    display_end = closing
                    break

        heading = re.match(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = re.sub(r"^\d+(?:\.\d+)*[.)]?\s*", "", heading.group(2)).strip().casefold()
            if reference_level is not None and level <= reference_level:
                reference_level = None
            if title in REFERENCE_NAMES:
                reference_level = level
                continue

        clean = mask_inline(line)
        if PLACEHOLDERS.search(clean):
            add(number, "DRAFT_PLACEHOLDER", "Resolve or retain only in an explicitly labeled working draft.", original)
        if "<!--" in line:
            add(number, "HIDDEN_COMMENT", "Inspect hidden comments for draft notes and identity information.", original)
        if reference_level is not None:
            continue
        if line.lstrip().startswith(">"):
            add(number, "QUOTATION_REVIEW", "Verify the quotation and source. Do not automatically rewrite exact quotations.", original)
            continue

        clean = re.sub(r"^(\s*(?:\*\*)?)Keywords:", r"\1Keywords", clean, count=1)
        checks = (
            (";" in clean, "PUNCT_SEMICOLON", "Replace the prose semicolon with a complete sentence."),
            (":" in clean, "PUNCT_COLON", "Review the prose colon. Keywords label and reference entries are exceptions."),
            (bool(re.search("[\u2013\u2014]", clean)), "PUNCT_LONG_DASH", "Rewrite prose without em or en dashes."),
            (bool(re.search(r"\s--\s", clean)), "PUNCT_DOUBLE_HYPHEN", "Do not use spaced double hyphens as prose separators."),
            (bool(CONTRACTIONS.search(clean)), "CONTRACTION", "Expand the contraction unless this is an exact protected source string."),
        )
        for matched, rule, message in checks:
            if matched:
                add(number, rule, message, original)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="UTF-8 .md or .txt manuscript files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable findings")
    parser.add_argument("--fail-on-findings", action="store_true", help="Return status 1 for any finding")
    args = parser.parse_args(argv)
    reports: list[dict[str, Any]] = []
    for path in args.files:
        if path.suffix.casefold() not in {".md", ".txt"}:
            parser.error(f"Unsupported format {path.suffix!r}. Use UTF-8 Markdown or plain text, not DOCX/PDF.")
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as error:
            parser.error(f"Cannot read {path}: {error}")
        reports.append({"file": str(path), "findings": lint_text(content)})
    total = sum(len(report["findings"]) for report in reports)
    if args.json:
        print(json.dumps({"heuristic_only": True, "total_findings": total,
                          "reports": reports}, ensure_ascii=False, indent=2))
    else:
        for report in reports:
            for item in report["findings"]:
                print(f"{report['file']}:{item['line']} {item['rule']} {item['message']}")
        print(f"{total} heuristic finding(s). Manual review is required. No files were changed.")
    return 1 if total and args.fail_on_findings else 0


if __name__ == "__main__":
    sys.exit(main())
