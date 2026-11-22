#!/usr/bin/env python3
"""Entry program for the news-image-20261122 bounty.

The judged image is the entry.png stored beside this file in the repository;
the program's only job is to copy it to /output/entry.png (or to the directory
named by MAKEFUN_OUTPUT_DIR when run outside the grader). Python 3 standard
library only, no network, deterministic.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
