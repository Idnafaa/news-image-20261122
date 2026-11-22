#!/usr/bin/env python3
"""news-image-20261122 entry program (v2).

The poster judged by make.fun is the entry.png committed next to this
file. Running the program simply copies that image into the grader's
output folder (/output by default, or $MAKEFUN_OUTPUT_DIR). It uses
nothing beyond the Python standard library, touches no network, and
produces the same bytes on every run.
"""

import os
import shutil
import sys


def main() -> int:
    base = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(base, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(image, os.path.join(target_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
