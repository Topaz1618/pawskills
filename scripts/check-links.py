#!/usr/bin/env python3
"""Check that every relative Markdown link in the repository resolves.

Links to external URLs are ignored. Links to files that do not exist are
reported as errors.

Usage:

    python scripts/check-links.py
    python scripts/check-links.py --quiet
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent

LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
STATUS_OK = "OK"
STATUS_ERROR = "ERROR"


def iter_markdown_files(root: Path) -> List[Path]:
    """Return every Markdown file under the given root."""
    return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)


def extract_links(text: str) -> List[str]:
    """Return every link target found in Markdown text."""
    targets: List[str] = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        targets.append(target)
    return targets


def is_external(target: str) -> bool:
    """Return True when the link points outside the repository."""
    parsed = urlparse(target)
    return bool(parsed.scheme) or target.startswith("//")


def check_links(root: Path) -> List[str]:
    """Return a list of broken link descriptions."""
    errors: List[str] = []
    for markdown_file in iter_markdown_files(root):
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append("{0}: could not be read ({1})".format(markdown_file, exc))
            continue
        for target in extract_links(text):
            if is_external(target):
                continue
            if target.startswith("#"):
                continue
            relative = unquote(urlparse(target).path)
            if not relative:
                continue
            resolved = (markdown_file.parent / relative).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(
                    "{0}: link '{1}' points outside the repository".format(
                        markdown_file.relative_to(root), target
                    )
                )
                continue
            if not resolved.exists():
                errors.append(
                    "{0}: link '{1}' does not resolve".format(
                        markdown_file.relative_to(root), target
                    )
                )
    return errors


def run(quiet: bool = False) -> int:
    errors = check_links(REPO_ROOT)
    if not quiet:
        if errors:
            for message in errors:
                print("[{0}] {1}".format(STATUS_ERROR, message))
        else:
            print("[{0}] links: no broken links found".format(STATUS_OK))
    if errors:
        print("")
        print("Found {0} broken link(s).".format(len(errors)))
        return 1
    print("Link check passed.")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-links.py",
        description="Check that every relative Markdown link in the repository resolves.",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print the final result.")
    args = parser.parse_args(argv)
    return run(quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
