#!/usr/bin/env python3
"""News in one image: 19 November 2026.

Entry program for make.fun news-image-20261119. The poster is drawn
in code by build_poster.py and stored here as entry.png; this program
just copies it to the output directory, deterministically.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
