import json
from pathlib import Path


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


PROJECT_ROOT = Path(__file__).resolve().parent.parent
