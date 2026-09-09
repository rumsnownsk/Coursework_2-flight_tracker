from typing import List, Dict, Any

import requests

from src.base_api import BaseApi


class AeroplanesAPI(BaseApi):
    def __init__(self) -> None:
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = None


    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        try:
            resp_nominatim = requests.get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
            resp_nominatim.raise_for_status()
            data = resp_nominatim.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Не удалось получить координаты для страны {country}: {e}")

        if not data:
            raise ValueError(f"Страна '{country}' не найдена в Nominatim")

        geo_data = data[0]
        boundingbox = geo_data.get("boundingbox")
        if not boundingbox or len(boundingbox) < 4:
            raise ValueError(f"Для страны '{country}' не удалось получить boundingbox")

        lamin, lamax, lomin, lomax = boundingbox[0], boundingbox[1], boundingbox[2], boundingbox[3]

        params_opensky = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax,
        }

        try:
            resp_opensky = requests.get(url=self.opensky_url, params=params_opensky)
            resp_opensky.raise_for_status()

            response = resp_opensky.json()

            try:
                self.aeroplanes = response["states"]
            except KeyError:
                raise KeyError("Ошибка структуры данных в ответе от opensky-network.org/api/states/all")



        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ошибка при запросе к OpenSky: {e}")

        return response or []
