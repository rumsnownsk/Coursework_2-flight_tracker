import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


@pytest.fixture
def saver(tmp_path):
    # Патчим именно src.json_saver.PROJECT_ROOT (имя скопировано туда при импорте)
    # tmp_path — уникальная папка для каждого теста, файл не накапливается
    with patch("src.json_saver.PROJECT_ROOT", new=tmp_path):
        yield JSONSaver("test_data.json")


def _add_planes(saver):
    p1 = Aeroplane("id1", "CS1", "RU", False, 800, 10000)
    p2 = Aeroplane("id2", "DLH", "DE", True, None, 5000)
    p3 = Aeroplane("id1", "CS2", "RU", False, 750, 9500)
    saver.add_aeroplane(p1)
    saver.add_aeroplane(p2)
    saver.add_aeroplane(p3)


# --------------------------------------------
# Добавление
# --------------------------------------------


def test_add_aeroplane_creates_file_and_adds_one(saver):
    plane = Aeroplane(
        id_flight="id1",
        callsign="CS1",
        reg_country="RU",
        on_ground=False,
        velocity=800,
        geo_altitude=10000,
    )
    saver.add_aeroplane(plane)

    data = saver.read_from_file()
    assert isinstance(data, dict)
    assert "states" in data
    assert len(data["states"]) == 1
    assert data["states"][0][0] == "id1"
    assert isinstance(data["time"], int)


def test_add_aeroplane_appends_multiple_records(saver):
    p1 = Aeroplane("id1", "CS1", "RU", False, 800, 10000)
    p2 = Aeroplane("id2", "DLH", "DE", True, None, 5000)

    saver.add_aeroplane(p1)
    saver.add_aeroplane(p2)

    data = saver.read_from_file()
    assert len(data["states"]) == 2
    assert data["states"][0][0] == "id1"
    assert data["states"][1][0] == "id2"


def test_add_aeroplane_handles_empty_file_structure(saver, tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("")

    with patch.object(JSONSaver, "full_path", new=bad_file):
        plane = Aeroplane("id3", "XYZ", "FR", False, 700, 9000)
        saver.add_aeroplane(plane)

        data = saver.read_from_file()
        assert isinstance(data, dict)
        assert len(data["states"]) == 1
        assert data["states"][0][0] == "id3"


# --------------------------------------------
# Удаление по id_flight
# --------------------------------------------


def test_delete_removes_all_matching(saver):
    _add_planes(saver)
    result = saver.delete_aeroplane("id1")
    assert "2" in result
    assert "id1" in result

    data = saver.read_from_file()
    assert len(data["states"]) == 1
    assert data["states"][0][0] == "id2"


def test_delete_removes_one(saver):
    p1 = Aeroplane("id1", "CS1", "RU", False, 800, 10000)
    p2 = Aeroplane("id2", "DLH", "DE", True, None, 5000)
    saver.add_aeroplane(p1)
    saver.add_aeroplane(p2)

    result = saver.delete_aeroplane("id2")
    assert "1" in result
    assert "id2" in result

    data = saver.read_from_file()
    assert len(data["states"]) == 1
    assert data["states"][0][0] == "id1"


def test_delete_not_found(saver):
    _add_planes(saver)
    result = saver.delete_aeroplane("idXYZ")
    assert "0" in result
    assert "idXYZ" in result

    data = saver.read_from_file()
    assert len(data["states"]) == 3


# --------------------------------------------
# Проверка на None
# --------------------------------------------


def test_delete_none_id_returns_message(saver):
    _add_planes(saver)
    result = saver.delete_aeroplane(None)
    assert "не передан" in result

    data = saver.read_from_file()
    assert len(data["states"]) == 3


# --------------------------------------------
# Нет файла / битый файл
# --------------------------------------------


def test_delete_no_file(saver):
    # Файл ещё не создан — read_from_file вернёт None
    result = saver.delete_aeroplane("id1")
    assert "Нет данных" in result


def test_delete_broken_file(saver, tmp_path):
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("{ invalid json }")

    with patch.object(JSONSaver, "full_path", new=bad_file):
        result = saver.delete_aeroplane("id1")
        assert "Нет данных states" in result or "0" in result
