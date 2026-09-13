import pytest
from unittest.mock import patch, MagicMock
from src.aeroplanes_api import AeroplanesAPI
import requests


@pytest.fixture
def api():
    return AeroplanesAPI()


# -------------------------
# Успешный сценарий
# -------------------------
@patch("requests.get")
def test_get_aeroplanes_success(mock_get, api):
    mock_nominatim_resp = MagicMock()
    mock_nominatim_resp.json.return_value = [
        {
            "boundingbox": ["10.0", "20.0", "30.0", "40.0"],
            "display_name": "Testland"
        }
    ]
    mock_nominatim_resp.raise_for_status.return_value = None

    mock_opensky_resp = MagicMock()
    mock_opensky_resp.json.return_value = {
        "states": [
            ["id1", "CS1", "RU", 0, 0, 0, 0, 0, False, 100, 0, 0, None, 5000, "1000", False, 0],
            ["id2", "CS2", "RU", 0, 0, 0, 0, 0, True, 0, 0, 0, None, 2000, "7670", False, 0]
        ]
    }
    mock_opensky_resp.raise_for_status.return_value = None

    mock_get.side_effect = [mock_nominatim_resp, mock_opensky_resp]

    result = api.get_aeroplanes("Russia")

    # возвращается весь response, а не только states
    assert result["states"] == mock_opensky_resp.json()["states"]
    assert api.aeroplanes == result["states"]


@patch("requests.get")
def test_get_aeroplanes_country_not_found(mock_get, api):
    mock_resp = MagicMock()
    mock_resp.json.return_value = []
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = api.get_aeroplanes("UnknownCountry")

    assert result == []
    mock_get.assert_called_once()


# -------------------------
# Нет boundingbox у страны
# -------------------------
@patch("requests.get")
def test_get_aeroplanes_no_boundingbox(mock_get, api):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"display_name": "WeirdCountry"}  # нет boundingbox
    ]
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    with pytest.raises(ValueError, match="не удалось получить boundingbox"):
        api.get_aeroplanes("WeirdCountry")


# -------------------------
# Ошибка сети на Nominatim
# -------------------------
@patch("requests.get")
def test_get_aeroplanes_nominatim_network_error(mock_get, api):
    mock_get.side_effect = requests.exceptions.ConnectionError("Boom")

    with pytest.raises(RuntimeError, match="Не удалось получить координаты"):
        api.get_aeroplanes("Russia")


# -------------------------
# Ошибка сети на OpenSky
# -------------------------
@patch("requests.get")
def test_get_aeroplanes_opensky_network_error(mock_get, api):
    # Первый запрос (Nominatim) — ок
    mock_nominatim = MagicMock()
    mock_nominatim.json.return_value = [
        {"boundingbox": ["0", "1", "0", "1"], "display_name": "SmallLand"}
    ]
    mock_nominatim.raise_for_status.return_value = None

    # Второй запрос (OpenSky) — ошибка
    mock_opensky = MagicMock()
    mock_opensky.raise_for_status.side_effect = requests.exceptions.Timeout("Timeout")
    mock_get.side_effect = [mock_nominatim, mock_opensky]

    with pytest.raises(RuntimeError, match="Ошибка при запросе к OpenSky"):
        api.get_aeroplanes("SmallLand")


# -------------------------
# Неверная структура OpenSky (нет states)
# -------------------------
@patch("requests.get")
def test_get_aeroplanes_bad_opensky_structure(mock_get, api):
    mock_nominatim = MagicMock()
    mock_nominatim.json.return_value = [
        {"boundingbox": ["0", "1", "0", "1"], "display_name": "BadStructLand"}
    ]
    mock_nominatim.raise_for_status.return_value = None

    mock_opensky = MagicMock()
    mock_opensky.json.return_value = {"other_key": "value"}  # нет states
    mock_opensky.raise_for_status.return_value = None
    mock_get.side_effect = [mock_nominatim, mock_opensky]

    with pytest.raises(KeyError, match="Ошибка структуры данных"):
        api.get_aeroplanes("BadStructLand")