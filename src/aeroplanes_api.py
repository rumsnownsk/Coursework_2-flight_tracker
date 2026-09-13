from typing import Any, Dict, List

import requests

from src.base_api import BaseApi


class AeroplanesAPI(BaseApi):
    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers_nominatim: Dict[str, str] = {
            "User-Agent": "test-app/1.0",
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim: Dict[str, Any] = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        try:
            resp_nominatim = requests.get(
                url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim
            )
            resp_nominatim.raise_for_status()
            data = resp_nominatim.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Не удалось получить координаты для страны {country}: {e}")

        if not data:
            return []
            # raise ValueError(f"Страна '{country}' не найдена в Nominatim")

        geo_data = data[0]

        bbox_raw = geo_data.get("boundingbox")
        if not isinstance(bbox_raw, list) or len(bbox_raw) < 4:
            raise ValueError(f"Для страны '{country}' не удалось получить boundingbox")

        bbox: List[float] = [float(x) for x in bbox_raw[:4]]
        lamin, lamax, lomin, lomax = bbox

        params_opensky: Dict[str, float] = {
            "lamin": float(lamin),
            "lamax": float(lamax),
            "lomin": float(lomin),
            "lomax": float(lomax),
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
