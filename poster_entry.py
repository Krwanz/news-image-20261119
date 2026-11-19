#!/usr/bin/env python3
"""Entry program for the 19 November 2026 front page.

The poster itself is drawn by build_poster.py and kept in this folder
as entry.png. This program only places a copy of that file in the
directory the harness names, so repeated runs produce identical bytes.
"""

import os
import shutil
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "entry.png"


def place_poster():
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy(POSTER, destination / "entry.png")


if __name__ == "__main__":
    place_poster()
