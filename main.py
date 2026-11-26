#!/usr/bin/env python3
"""Entry program for "Sum up 25 November's world news in one image".

entry.png, stored beside this file, is a one-page newspaper front page
for Wednesday 25 November 2026. It was typeset by compose_winners.py from
the story data in winners_data.py / final_data.py (kept here). This program
copies that image, byte for byte, to /output/entry.png.

Standard library only, no network, identical bytes on every run.
For a local dry run outside the grading container, point
MAKEFUN_OUTPUT_DIR at a folder of your choice:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().with_name("entry.png"),
                    target_dir / "entry.png")


if __name__ == "__main__":
    main()
