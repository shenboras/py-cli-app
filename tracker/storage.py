import json
from pathlib import Path
from tracker.exceptions import StorageError

def load_expenses(file_path):
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        content = path.read_text(encoding="utf-8").strip()
        if content == "":
            return []

        data = json.loads(content)
        if not isinstance(data, list):
            raise StorageError("JSON file must contain a list.")


        return data
    except json.JSONDecodeError:
        raise StorageError("JSON file is corrupted and cannot be read.")
    except OSError:
        raise StorageError("An error occured while reading the file.")


def save_expenses(file_path ,expenses):
    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        json_text = json.dumps(expenses, indent=2, ensure_ascii=False)
        path.write_text(json_text, encoding="utf-8")
    except OSError:
        raise StorageError("An error occured while writing to the file.")
            