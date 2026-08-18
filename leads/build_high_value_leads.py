#!/usr/bin/env python3
"""Rebuild the DMC Client Console from Gulf verified leads."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\FPIN\Desktop\dm os\leads")


def main() -> None:
    subprocess.check_call([sys.executable, str(ROOT / "generate_high_value_outreach.py")])


if __name__ == "__main__":
    main()
