import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
WAIT = int(os.getenv("WAIT", "10"))

SCREENSHOT_DIR = ROOT / "reports" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
