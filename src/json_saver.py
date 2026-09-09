import json
from abc import ABC
from pathlib import Path

from src import aeroplanes_api
from src.aeroplanes_api import AeroplanesAPI
from src.base_file import BaseFile
from src.helpers import PROJECT_ROOT


class JSONSaver(BaseFile):

    def __init__(self, filepath:str|Path= "data.json"):
        super().__init__(filepath)

        self.base_dir = PROJECT_ROOT / "data"
        # Папку создаём сразу при инициализации (один раз), чтобы дальше не проверять
        self.base_dir.mkdir(parents=True, exist_ok=True)


    def write_to_file(self, data):
        with open(f"{self.base_dir}/{self.filepath}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def read_from_file(self, filepath):
        with open(f"{self.base_dir}/ {self.filepath}") as f:
            pass

    def add_aeroplane(self, filepath):
        pass

    def delete_aeroplanes(self, filepath):
        pass



if __name__ == "__main__":
    json_saver = JSONSaver()
    json_saver.write_to_file()