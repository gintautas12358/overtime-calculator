import pandas as pd
from datetime import timedelta
from pathlib import Path
from argparse import ArgumentParser

DAY_TO_HOURS = 24
MIN_TO_SECONDS = 60
HOURS_TO_MINUTES = 60
HOURS_TO_SECONDS = HOURS_TO_MINUTES * MIN_TO_SECONDS
WORKING_DAY_DURATION_H = 8
WORKING_DAY_DURATION_S = WORKING_DAY_DURATION_H * HOURS_TO_SECONDS
BREAK_TIME_MIN = 30
BREAK_TIME_SECONDS = BREAK_TIME_MIN * MIN_TO_SECONDS


def get_data(file_path: Path, config: dict) -> tuple[int, int]:
    """
    Extracts required and total work hours from a CSV file.
    """
    df = pd.read_csv(file_path)
    df = df.reset_index()  # make sure indexes pair with number of rows

    day_dict = {}
    for _, row in df.iterrows():
        day_dict[row["Date"]] = day_dict.get(row["Date"], 0) + row["Duration"]

    size = len(day_dict)
    total_duration = sum(day_dict.values()) - size * (
        config.get("remove_breaks") * BREAK_TIME_SECONDS
    )
    required_duration = WORKING_DAY_DURATION_S * size

    return required_duration, total_duration


def calc_overtime(required_duration, total_duration):
    """
    Calculate overtime.
    """
    td = timedelta(seconds=int(total_duration - required_duration))
    hours, minutes = (
        td.days * DAY_TO_HOURS + td.seconds // HOURS_TO_SECONDS,
        (td.seconds // MIN_TO_SECONDS) % HOURS_TO_MINUTES,
    )
    return hours, minutes


def estimate(file_path: str, config: dict) -> None:
    """
    Calculate overtime or undertime based on work hours.
    """

    required_duration, total_duration = get_data(file_path, config)

    hours, minutes = calc_overtime(required_duration, total_duration)
    if total_duration > required_duration:
        free_days = hours // WORKING_DAY_DURATION_H
        print(f"Overtime: {hours}:{minutes}:00")
        print(f"Eligible free days: {free_days}")
        print(
            f"Eligible not full day: {hours - WORKING_DAY_DURATION_H*(free_days)}:{minutes}:00"
        )

    else:
        print(f"Undertime: {hours}:{minutes}:00")


def main():
    parser = ArgumentParser(
        description="Calculate overtime or undertime based on work hours."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Path to the CSV file containing work hours.",
    )
    parser.add_argument(
        "-r",
        "--remove-breaks",
        action="store_true",
        help="Remove breaks from the calculation.",
    )
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    config = {
        "remove_breaks": 1 if args.remove_breaks else 0,
    }
    estimate(file_path, config)


if __name__ == "__main__":
    main()
