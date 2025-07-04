import pandas as pd
from datetime import timedelta
from pathlib import Path
from argparse import ArgumentParser


def hours_minutes(td: timedelta) -> tuple[int, int]:
    return td.days * 24 + td.seconds // 3600, (td.seconds // 60) % 60


def main(file_path: str) -> None:
    """
    Calculate overtime or undertime based on work hours.
    """

    df = pd.read_csv(file_path)
    df = df.reset_index()  # make sure indexes pair with number of rows

    day_dict = {}
    for index, row in df.iterrows():
        day_dict[row["Date"]] = day_dict.get(row["Date"], 0) + row["Duration"]

    size = len(day_dict)
    total_duration = sum(day_dict.values())
    working_day_duration_h = 8
    hours_to_seconds = 60 * 60
    working_day_duration_s = working_day_duration_h * hours_to_seconds
    required_duration = working_day_duration_s * size

    overtime = timedelta(seconds=int(total_duration - required_duration))
    hours, minutes = hours_minutes(overtime)
    if total_duration > required_duration:
        print(f"Overtime: {hours}:{minutes}:00")  #
        print(f"Eligible free days: {hours // working_day_duration_h}")
        print(
            f"Eligible not full day: {hours - working_day_duration_h*(hours // working_day_duration_h)}:{minutes}:00"
        )

    else:
        print(f"Undertime: {hours}:{minutes}:00")


if __name__ == "__main__":
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
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    main(file_path)
