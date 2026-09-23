"""读取数据文件提供给测试使用。"""
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def read_csv(name):
    path = DATA_DIR / name
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))