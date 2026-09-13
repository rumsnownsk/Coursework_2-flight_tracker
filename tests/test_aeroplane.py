import pytest

from src.aeroplane import Aeroplane


# ============================
# Фикстуры
# ============================
@pytest.fixture
def sample_states():
    """Сырые данные API: 2 нормальных самолёта + 1 мусорная строка."""
    return [
        ["id1", "AFL123", "Russia", 0, 0, 0, 0, 0, False, 800, 0, 0, None, 10000, "1000", False, 0],
        ["id2", "DLH456", "Germany", 0, 0, 0, 0, 0, True, 0, 0, 0, None, 5000, "7670", False, 0],
        ["short_row"],  # мусор — должен пропуститься
    ]


@pytest.fixture
def plane_high():
    return Aeroplane("id1", "AFL123", "Russia", False, 800, 10000)


@pytest.fixture
def plane_low():
    return Aeroplane("id2", "DLH456", "Germany", True, 0, 5000)


def test_create_valid_plane():
    plane = Aeroplane("id1", "CS1", "Russia", False, 800.5, 10000.0)
    assert plane.id_flight == "id1"
    assert plane.reg_country == "Russia"
    assert plane.on_ground is False

@pytest.mark.parametrize("bad_id, expected_error", [
    (123, "id_flight"),
    (None, "id_flight"),
    ([], "id_flight"),
])
def test_invalid_id_flight(bad_id, expected_error):
    with pytest.raises(TypeError, match=expected_error):
        Aeroplane(id_flight=bad_id)


@pytest.mark.parametrize("bad_velocity", ["800", [], True, False])
def test_invalid_velocity(bad_velocity):
    with pytest.raises(TypeError, match="velocity"):
        Aeroplane(velocity=bad_velocity)


@pytest.mark.parametrize("bad_altitude", ["10000", [], True, False])
def test_invalid_altitude(bad_altitude):
    with pytest.raises(TypeError, match="geo_altitude"):
        Aeroplane(geo_altitude=bad_altitude)


# ============================
# Тесты cast_to_object_list
# ============================

def test_cast_valid_states(sample_states):
    planes = Aeroplane.cast_to_object_list(sample_states)
    assert len(planes) == 2
    assert planes[0].id_flight == "id1"
    assert planes[1].geo_altitude == 5000

# ============================
# Тесты сравнения по высоте
# ============================

def test_greater_than(plane_high, plane_low):
    assert plane_high > plane_low


def test_less_than(plane_high, plane_low):
    assert plane_low < plane_high


def test_equal_altitude():
    p1 = Aeroplane("1", "A", "RU", False, 100, 10000)
    p2 = Aeroplane("2", "B", "RU", False, 200, 10000)
    assert p1 == p2


def test_comparison_with_non_aeroplane_raises(plane_high):
    with pytest.raises(TypeError):
        _ = plane_high > 100


# ============================
# Тесты сравнения по скорости
# ============================

def test_is_faster_than_true(plane_high, plane_low):
    assert plane_high.is_faster_than(plane_low) is True


def test_is_faster_than_false(plane_low, plane_high):
    assert plane_low.is_faster_than(plane_high) is False


# ============================
# Тест __str__
# ============================

def test_str_contains_fields(plane_high):
    s = str(plane_high)
    assert "id1" in s
    assert "AFL123" in s
    assert "Russia" in s


def test_str_on_ground_yes():
    plane = Aeroplane("id", "CS", "RU", True, 0, 0)
    assert "да" in str(plane)


def test_str_on_ground_no(plane_high):
    assert "нет" in str(plane_high)



