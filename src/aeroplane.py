from typing import List, Any

class Aeroplane:
    """
        Модель самолёта для работы с данными OpenSky API.

        Атрибуты:
            id_flight (str): уникальный идентификатор рейса (ICAO24).
            callsign (str): позывной рейса (например, "THA110").
            reg_country (str): страна регистрации.
            on_ground (bool): находится ли самолёт на земле.
            velocity (float): горизонтальная скорость (м/с).
            geo_altitude (float): геометрическая высота (м).
    """
    def __init__(
            self,
            id_flight: str = "",
            callsign: str = "",  # позывной рейса
            reg_country: str = "",  # Страна регистрации
            on_ground: bool = True,  # находится ли самолёт на земле
            velocity: float = 0.0,  # горизонтальная скорость
            geo_altitude: float = 0.0 # геометрическая высота (м)
    ):
        if velocity is None:
            velocity = 0
        Aeroplane.__validate(id_flight, reg_country, callsign, on_ground, velocity, geo_altitude)
        self.id_flight = id_flight
        self.callsign = callsign
        self.reg_country = reg_country
        self.on_ground = on_ground
        self.velocity = velocity
        self.geo_altitude = geo_altitude

    @classmethod
    def cast_to_object_list(cls, states: list[list]) -> list["Aeroplane"]:
        """
        Преобразует сырые данные API (список списков) в список объектов Aeroplane.

        Args:
            states: Список списков из поля "states" ответа OpenSky API.

        Returns:
            Список объектов Aeroplane. Строки с длиной < 16 пропускаются.
        """
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
        """Валидирует типы аргументов при создании объекта. Выбрасывает TypeError при несоответствии."""
        if not isinstance(id_flight, str):
            raise TypeError(f"id_flight должно быть строкой, а приходит <{type(id_flight).__name__}>")

        if not isinstance(reg_country, str):
            raise TypeError(f"reg_country должен быть строкой, а получено <{type(reg_country).__name__}>")

        if not isinstance(callsign, str):
            raise TypeError(f"callsign должен быть строкой, а получено <{type(callsign).__name__}>")

        if not isinstance(on_ground, bool):
            raise TypeError(f"on_ground должен быть BOOL, а получено <{type(on_ground).__name__}>")

        if isinstance(velocity, bool) or not isinstance(velocity, (int, float)):
            raise TypeError(f"velocity должен быть числом (int/float), а получено <{type(velocity).__name__}>")

        if isinstance(geo_altitude, bool) or not isinstance(geo_altitude, (int, float)):
            raise TypeError(
                f"geo_altitude должен быть числом (int/float), а получено <{geo_altitude} as {type(geo_altitude).__name__}>")

    def __str__(self):
        """Возвращает строковое представление самолёта для вывода в консоль."""
        return (f"# {self.id_flight} | "
                f"Позывной: {self.callsign or ' '*8} | "
                f"Высота: {str(self.geo_altitude or 0).ljust(10)} | " 
                f"На земле: {(' да' if self.on_ground else 'нет').ljust(4)} | " 
                f"Скорость: {str(self.velocity or 0).ljust(10)} | "
                f"Страна(рег.): {(self.reg_country or "").ljust(12)}"
                )

    def __lt__(self, other: "Aeroplane") -> bool:
        """self < other: self находится НИЖЕ, чем other."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude < other.geo_altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """self > other: self находится ВЫШЕ, чем other."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude > other.geo_altitude

    def __le__(self, other: "Aeroplane") -> bool:
        """self <= other: self ниже или на той же высоте, что other."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude <= other.geo_altitude

    def __ge__(self, other: "Aeroplane") -> bool:
        """self >= other: self выше или на той же высоте, что other."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude >= other.geo_altitude

    def __eq__(self, other: object) -> bool:
        """self == other: высоты равны."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.geo_altitude == other.geo_altitude

    def is_faster_than(self, other: "Aeroplane") -> bool:
        """Возвращает True, если self быстрее other."""
        return self.velocity > other.velocity