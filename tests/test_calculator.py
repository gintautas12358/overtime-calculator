from pathlib import Path
import pytest

from overtime_calculator.main import get_data, data_to_time, calc_overtime, estimate


@pytest.fixture
def create_csv_file(tmp_path):
    """
    Create a temporary CSV file for testing.
    """
    data = """Date,Duration
2023-01-01,12
2023-01-01,2
2023-01-01,3
2023-01-01,4
2023-01-02,9
2023-01-03,7
"""
    csv_file = tmp_path / "test_data.csv"
    with open(csv_file, "w") as f:
        f.write(data)

    return csv_file


def test_get_data(create_csv_file):
    """
    Test the get_data function to ensure it reads the CSV file correctly.
    """
    data = get_data(create_csv_file)
    expected_data = {
        "2023-01-01": 21,
        "2023-01-02": 9,
        "2023-01-03": 7,
    }
    assert data == expected_data


def test_data_to_time_no_break():
    """
    Test the data_to_time function to ensure it calculates required and total durations correctly.
    """

    hours_to_seconds = 3600
    day_dict = {
        "2023-01-01": 9 * hours_to_seconds,
        "2023-01-02": 10 * hours_to_seconds,
        "2023-01-03": 11 * hours_to_seconds,
    }
    config = {"remove_breaks": 0}  # Assuming breaks are not removed
    required_duration, total_duration = data_to_time(day_dict, config)

    assert required_duration == 8 * 3 * 3600  # 8 hours per day * 3 days
    assert total_duration == 30 * hours_to_seconds


def test_data_to_time_with_break():
    """
    Test the data_to_time function to ensure it calculates required and total durations correctly with breaks.
    """

    hours_to_seconds = 3600
    day_dict = {
        "2023-01-01": 9 * hours_to_seconds,
        "2023-01-02": 10 * hours_to_seconds,
        "2023-01-03": 11 * hours_to_seconds,
    }
    config = {"remove_breaks": 1}  # Assuming breaks are removed
    required_duration, total_duration = data_to_time(day_dict, config)

    assert required_duration == 8 * 3 * 3600
    assert total_duration == 30 * hours_to_seconds - 3 * 30 * 60


def test_calc_overtime():
    """
    Test the calc_overtime function to ensure it calculates overtime correctly.
    """
    required_duration = 24 * 3600
    total_duration = 30 * 3600 + 2 * 60

    hours, minutes = calc_overtime(required_duration, total_duration)

    assert hours == 6
    assert minutes == 2
