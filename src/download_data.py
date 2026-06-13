"""Download the Bank Customer Churn dataset into data/raw/.

The raw CSV is committed to the repo for reproducibility, so this script is only
needed if you want to re-fetch it from scratch.
"""

import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/sharmaroshan/"
    "Churn-Modelling-Dataset/master/Churn_Modelling.csv"
)
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
TARGET = RAW_DIR / "Churn_Modelling.csv"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if TARGET.exists():
        print(f"Already present: {TARGET}")
        return

    print(f"Downloading {SOURCE_URL} ...")
    urllib.request.urlretrieve(SOURCE_URL, TARGET)
    print(f"Saved {TARGET} ({TARGET.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
