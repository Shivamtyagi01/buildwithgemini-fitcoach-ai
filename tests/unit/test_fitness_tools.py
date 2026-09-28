"""Unit tests for fitness computation tools."""

from app.fitness_tools import calculate_1rm_and_zones


def test_calculate_1rm_and_zones_valid():
    result = calculate_1rm_and_zones(225.0, 5)
    assert "257.8 lbs" in result
    assert "Heavy Strength" in result
    assert "Hypertrophy Zone" in result


def test_calculate_1rm_and_zones_single_rep():
    result = calculate_1rm_and_zones(300.0, 1)
    assert "300.0 lbs" in result


def test_calculate_1rm_and_zones_invalid():
    result = calculate_1rm_and_zones(0, 5)
    assert "Error" in result
