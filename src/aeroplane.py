import json
from typing import List, Any

from mypy.config_parser import convert_to_boolean

from src.helpers import print_json
from src.json_saver import JSONSaver


class Aeroplane:

    # __aeroplanes_list = []

    def __init__(
            self,
            id_flight: str = "",
            callsign: str = "",  # позывной рейса
            reg_country: str = "",  # Страна регистрации
            on_ground: bool = True,  # находится ли самолёт на земле
            velocity: float = 0.0,  # горизонтальная скорость
            geo_altitude: float = 0.0 # геометрическая высота (м)
    ):
        Aeroplane.__validate(id_flight, reg_country, callsign, on_ground, velocity, geo_altitude)

        self.id_flight = id_flight
        self.callsign = callsign
        self.reg_country = reg_country
        self.on_ground = on_ground
        self.velocity = velocity
        self.geo_altitude = geo_altitude

    @classmethod
    def cast_to_object_list(cls, states: list[list]) -> list["Aeroplane"]:
        """ приведение к списку объектов """
        result: List["Aeroplane"] = []

        for item in states:
            if not isinstance(item, list) or len(item) < 16:
                continue
            result.append(cls(
                id_flight=item[0],
                callsign = item[1],
                reg_country = item[2],
                on_ground = item[8],
                velocity = item[9],
                geo_altitude = item[13] if isinstance(item[13], (int, float)) else 0.0

            ))
        return result

    @staticmethod
    def __validate(id_flight, reg_country, callsign, on_ground, velocity, geo_altitude) -> None:
        if not isinstance(id_flight, str):
            raise TypeError(f"id_flight должно быть строкой, а приходит <{type(id_flight).__name__}>")

        if not isinstance(reg_country, str):
            raise TypeError(f"reg_country должен быть строкой, а получено <{type(reg_country).__name__}>")

        if not isinstance(callsign, str):
            raise TypeError(f"callsign должен быть строкой, а получено <{type(callsign).__name__}>")

        if not isinstance(on_ground, bool):
            raise TypeError(f"on_ground должен быть BOOL, а получено <{type(on_ground).__name__}>")

        if not isinstance(velocity, (int, float)):
            raise TypeError(f"velocity должен быть числом (int/float), а получено <{type(velocity).__name__}>")

        if not isinstance(geo_altitude, (int, float)):
            raise TypeError(f"geo_altitude должен быть числом (int/float), а получено <{geo_altitude} as {type(geo_altitude).__name__}>")

    def __str__(self):
        return f"Рейс # {self.id_flight} | Позывной: {self.callsign} | Страна: {self.reg_country}| Высота: {self.geo_altitude}"

    def __lt__(self, other:"Aeroplane") -> bool:
        """
        сравнение по высоте
        self < other: self находится НИЖЕ, чем other
        :param other:
        :return: bool
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude < other.geo_altitude

    def __gt__(self, other) -> bool:
        """
        сравнение по высоте.
        self > other: self находится ВЫШЕ, чем other
        :param other:
        :return: bool
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude > other.geo_altitude