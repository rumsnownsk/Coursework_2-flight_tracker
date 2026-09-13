import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, cast

from src.aeroplane import Aeroplane
from src.base_file import BaseFile
from src.helpers import PROJECT_ROOT


class JSONSaver(BaseFile):

    def __init__(self, filepath: str | Path = "data.json"):
        super().__init__(filepath)

        # Вычисляем base_dir сразу, но не создаём папку прямо здесь — сделаем это в отдельном методе
        self.base_dir = PROJECT_ROOT / "data"

        # Поле для хранения данных
        self.data: list | dict | None = None

    @property
    def full_path(self) -> Path:
        """Возвращает полный путь к файлу: base_dir + имя файла."""
        fp = Path(self.filepath)
        if fp.is_absolute():
            return fp
        return self.base_dir / fp.name

    def ensure_data_dir(self):
        """Создаёт папку data, если её нет."""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_to_file(self, data):
        """Записывает словарь data в JSON-файл по полному пути.
        Папка создаётся автоматически. Файл перезаписывается полностью.
        """
        path = self.full_path
        # Сначала убедимся, что папка есть
        self.ensure_data_dir()

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def read_from_file(self) -> Optional[Dict[str, Any]]:
        """Читает JSON-файл и возвращает содержимое как dict.

        - Если файла нет — возвращает None.
        - Если файл пустой или битый — возвращает базовую структуру:
          {"time": <unix>, "country": "---", "states": []}.
        """
        path = self.full_path

        # Если файла вообще нет — возвращаем None, дальше add_aeroplane сам создаст структуру
        if not path.exists():
            return None

        try:
            # Используем path.open, чтобы это было удобно мокать через patch("pathlib.Path.open")
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return cast(Dict[str, Any], data)
        except (json.JSONDecodeError, ValueError):
            # Файл есть, но невалидный JSON (пустой или битый)
            # Возвращаем «чистую» структуру, чтобы add_aeroplane мог работать
            return {"time": int(datetime.now().timestamp()), "country": "---", "states": []}

    def add_aeroplane(self, aeroplane: "Aeroplane") -> None:
        """Добавляет одну запись о самолёте в JSON-файл.

        Запись — это список из 17 полей (формат OpenSky states), где первым элементом
        является aeroplane.id_flight.

        Поведение:
        - Если файла нет или он битый — создаётся новая структура.
        - Запись добавляется в конец списка states.
        - Поле time обновляется до текущего UNIX-времени.
        """
        raw = self.read_from_file()

        # Если файла нет / пусто / не словарь — создаём правильную структуру
        if raw is None or not isinstance(raw, dict):
            raw = {"time": int(datetime.now().timestamp()), "country": "---", "states": []}

        # Если ключа "states" нет — добавляем
        if "states" not in raw:
            raw["states"] = []

        raw["states"].append(
            [
                aeroplane.id_flight,  # 0
                aeroplane.callsign,  # 1
                aeroplane.reg_country,  # 2
                None,  # 3 — time_position
                None,  # 4 — last_contact
                None,  # 5 — longitude
                None,  # 6 — latitude
                None,  # 7 — baro_altitude
                aeroplane.on_ground,  # 8
                aeroplane.velocity,  # 9
                None,  # 10 — heading
                None,  # 11 — vertical_rate
                None,  # 12 — sensors
                aeroplane.geo_altitude,  # 13
                None,  # 14 — squawk
                False,  # 15 — spi
                0,  # 16 — position_source
            ]
        )
        raw["time"] = int(datetime.now().timestamp())
        self.write_to_file(raw)

    def delete_aeroplane(self, id_flight: str | None = None) -> str:
        """Удаляет все записи с указанным id_flight из JSON-файла.
        Удаляет по совпадению с первым элементом записи (индекс 0 — id_flight).
        Возвращает количество удалённых записей.
        """
        if id_flight is None:
            return "Позывной < id_flight > не передан"

        data = self.read_from_file()

        if data is None or not isinstance(data, dict):
            return "Нет данных для удаления"

        states = data.get("states")
        if not isinstance(states, list):
            return "Нет данных states для удаления"

        before_len = len(states)

        # Оставляем только те, у которых id_flight НЕ совпадает
        new_states = [p for p in states if p[0] != id_flight]

        after_len = len(new_states)
        removed_count = before_len - after_len
        data["states"] = new_states

        self.write_to_file(data)
        return f"Удалены записи по позывному < {id_flight} >: {removed_count} шт."
