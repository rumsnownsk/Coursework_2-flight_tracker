import json
from pathlib import Path

from src.base_file import BaseFile
from src.helpers import PROJECT_ROOT


class JSONSaver(BaseFile):

    def __init__(self, filepath:str|Path= "data.json"):
        super().__init__(filepath)

        self.base_dir = PROJECT_ROOT / "data"
        # Папку создаём сразу при инициализации (один раз), чтобы дальше не проверять
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Поле для хранения данных (чтобы write_to_file не требовал аргумент)
        self.data: list | dict | None = None

    @property
    def full_path(self) -> Path:
        """Возвращает полный путь к файлу: base_dir + имя файла."""
        # Если filepath уже абсолютный — возвращаем его, иначе собираем
        fp = Path(self.filepath)
        if fp.is_absolute():
            return fp
        return self.base_dir / fp.name

    def write_to_file(self, data):
        path = self.full_path

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def read_from_file(self):
        """
        Читаем JSON из файла и возвращает содержимое как Python-объект.
        """
        path = self.full_path
        if not path.exists():
            return None
        try:
            with open(f"{self.base_dir}/{self.filepath}") as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            raise ValueError(f"Не удалось прочитать JSON из {path}: {e}") from e

    def add_aeroplane(self):
        pass

    def delete_aeroplanes(self):
        pass



# if __name__ == "__main__":
#     json_saver = JSONSaver()
#     json_saver.write_to_file()