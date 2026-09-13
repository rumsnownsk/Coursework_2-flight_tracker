import re
from typing import List

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


class FlightManager:

    # filtered_aeroplanes = []

    def __init__(self, aeroplanes: list[Aeroplane]):
        # Храним только объекты Aeroplane, никаких сырых списков
        self.aeroplanes: List[Aeroplane] = aeroplanes or []
        # Здесь будем хранить результат фильтрации
        self.filtered_aeroplanes: List[Aeroplane] = self.aeroplanes

    def load_from_file(self):
        """
        Метод загружает данные по самолётам из файла в атрибут self.__aeroplanes_list
        :return:
        """
        json_saver = JSONSaver()
        raw = json_saver.read_from_file()

        if not isinstance(raw, dict):
            self.aeroplanes = []
            self.filtered_aeroplanes = []
            return

        states = raw.get("states", [])
        # Превращаем сырые данные в объекты
        self.aeroplanes = Aeroplane.cast_to_object_list(states)
        # После загрузки сбрасываем фильтр на полный список
        self.filtered_aeroplanes = self.aeroplanes[:]

    def get_top_aeroplanes(self, top_n):
        if not top_n:
            return

        try:
            n = int(top_n)
        except (ValueError, TypeError):
            print("Кол-во самолётов должно быть числом. Выведется весь список\n")
            return

        if n < 0:
            return

        self.filtered_aeroplanes = self.filtered_aeroplanes[:n]

    def filter_by_reg_country(self, reg_countries: list):
        """фильтрация самолётов по стране-регистрации"""
        if not reg_countries:
            return

        normalize_countries = [c.strip().lower() for c in reg_countries]

        res = [a for a in self.filtered_aeroplanes if a.reg_country.lower() in normalize_countries]

        self.filtered_aeroplanes = res
        return

    def filter_by_altitude(self, altitude_range: str):
        if not altitude_range:
            return
        match = re.search(r"(\d+)\s*-\s*(\d+)", altitude_range)

        if match:
            min_val = int(match.group(1))
            max_val = int(match.group(2))
            if max_val < min_val:
                return

            self.filtered_aeroplanes = [a for a in self.filtered_aeroplanes if min_val < a.geo_altitude < max_val]
            return
        return

    def sort_aeroplanes_by_altitude(self, confirm):
        if confirm.lower() == "y":
            self.filtered_aeroplanes = sorted(self.filtered_aeroplanes, key=lambda p: p.geo_altitude, reverse=True)
            return
        return

    def __str__(self):
        return f"отфильтрованный итоговый список: {self.filtered_aeroplanes}"
