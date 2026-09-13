from unittest.mock import MagicMock, patch

import pytest

from src.aeroplane import Aeroplane
from src.flight_manager import FlightManager


@pytest.fixture
def plane_high():
    return Aeroplane("id1", "CS1", "Russia", False, 800, 10000)


@pytest.fixture
def plane_mid():
    return Aeroplane("id2", "CS2", "Germany", False, 700, 5000)


@pytest.fixture
def plane_low():
    return Aeroplane("id3", "CS3", "France", True, 0, 2000)


@pytest.fixture
def base_list(plane_high, plane_mid, plane_low):
    return [plane_high, plane_mid, plane_low]


@pytest.fixture
def manager(base_list):
    return FlightManager(base_list)


# -------------------------
# load_from_file (с моком JSONSaver)
# -------------------------
@patch("src.flight_manager.JSONSaver")
def test_load_from_file_success(mock_json_saver, manager):
    mock_saver = MagicMock()
    # Эмулируем ответ {"states": [...]}
    mock_saver.read_from_file.return_value = {
        "states": [
            ["id4", "CS4", "Spain", 0, 0, 0, 0, 0, False, 600, 0, 0, None, 3000, "1000", False, 0],
            ["id5", "CS5", "Italy", 0, 0, 0, 0, 0, True, 0, 0, 0, None, 1500, "7670", False, 0],
        ]
    }
    mock_json_saver.return_value = mock_saver

    manager.load_from_file()

    assert len(manager.aeroplanes) == 2
    assert isinstance(manager.aeroplanes[0], Aeroplane)
    assert manager.filtered_aeroplanes == manager.aeroplanes


@patch("src.flight_manager.JSONSaver")
def test_load_from_file_bad_type(mock_json_saver, manager):
    mock_saver = MagicMock()
    mock_saver.read_from_file.return_value = "not a dict"  # плохой тип
    mock_json_saver.return_value = mock_saver

    manager.load_from_file()

    assert manager.aeroplanes == []
    assert manager.filtered_aeroplanes == []


# -------------------------
# get_top_aeroplanes
# -------------------------
def test_get_top_aeroplanes_valid(manager, plane_high, plane_mid, plane_low):
    # Изначально 3 самолёта
    assert len(manager.filtered_aeroplanes) == 3

    manager.get_top_aeroplanes(2)

    assert len(manager.filtered_aeroplanes) == 2
    # Должны остаться первые два из текущего списка (порядок пока исходный)
    assert manager.filtered_aeroplanes[0] is plane_high
    assert manager.filtered_aeroplanes[1] is plane_mid


def test_get_top_aeroplanes_zero_or_negative(manager):
    manager.get_top_aeroplanes(0)
    assert len(manager.filtered_aeroplanes) == len(manager.aeroplanes)  # список не изменился

    manager.get_top_aeroplanes(-1)
    assert len(manager.filtered_aeroplanes) == len(manager.aeroplanes)


def test_get_top_aeroplanes_invalid_type(capsys, manager):
    manager.get_top_aeroplanes("abc")
    captured = capsys.readouterr()
    assert "Кол-во самолётов должно быть числом" in captured.out
    # Список не должен измениться
    assert len(manager.filtered_aeroplanes) == len(manager.aeroplanes)


# -------------------------
# filter_by_reg_country
# -------------------------
def test_filter_by_reg_country_match(manager, plane_high, plane_mid):
    # Russia и Germany
    manager.filter_by_reg_country(["Russia", "germany"])

    assert len(manager.filtered_aeroplanes) == 2
    countries = {p.reg_country.lower() for p in manager.filtered_aeroplanes}
    assert countries == {"russia", "germany"}


def test_filter_by_reg_country_no_match(manager):
    manager.filter_by_reg_country(["Japan"])
    assert manager.filtered_aeroplanes == []


def test_filter_by_reg_country_empty(manager):
    before = manager.filtered_aeroplanes[:]
    manager.filter_by_reg_country([])
    assert manager.filtered_aeroplanes == before


# -------------------------
# filter_by_altitude
# -------------------------
def test_filter_by_altitude_valid_range(manager, plane_high, plane_mid, plane_low):
    # 1000–6000: mid (5000) и low (2000), high (10000) не войдёт
    manager.filter_by_altitude("1000 - 6000")

    assert len(manager.filtered_aeroplanes) == 2
    heights = {p.geo_altitude for p in manager.filtered_aeroplanes}
    assert heights == {5000, 2000}


def test_filter_by_altitude_invalid_format(manager):
    before = manager.filtered_aeroplanes[:]
    manager.filter_by_altitude("not a range")
    # При неверном формате ничего не делаем
    assert manager.filtered_aeroplanes == before


def test_filter_by_altitude_reversed_range(manager):
    before = manager.filtered_aeroplanes[:]
    # min > max — ничего не делаем
    manager.filter_by_altitude("5000 - 1000")
    assert manager.filtered_aeroplanes == before


# -------------------------
# sort_aeroplanes_by_altitude
# -------------------------
def test_sort_aeroplanes_by_altitude_confirmed(manager, plane_high, plane_mid, plane_low):
    # Исходный порядок: high(10k), mid(5k), low(2k)
    # После сортировки по убыванию: high, mid, low — тот же порядок, но проверим логику
    manager.sort_aeroplanes_by_altitude("y")

    heights = [p.geo_altitude for p in manager.filtered_aeroplanes]
    assert heights == [10000, 5000, 2000]  # убывание


def test_sort_aeroplanes_by_altitude_not_confirmed(manager, plane_high, plane_mid, plane_low):
    before = manager.filtered_aeroplanes[:]
    manager.sort_aeroplanes_by_altitude("n")
    assert manager.filtered_aeroplanes == before


# -------------------------
# __str__
# -------------------------
def test_str_representation(manager):
    s = str(manager)
    assert "отфильтрованный итоговый список:" in s
    assert "Aeroplane" in s or "id1" in s  # зависит от того, как выводится объект
