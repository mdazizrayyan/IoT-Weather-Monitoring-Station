"""
data_logger.py
----------------
Handles writing timestamped weather readings to a local CSV file.
Creates the file with headers if it doesn't already exist.
"""

import csv
import os
from datetime import datetime

CSV_HEADERS = [
    "timestamp",
    "temperature_c",
    "humidity_percent",
    "pressure_hpa",
    "probe_temperature_c",
    "wind_speed_kmh",
    "wind_direction",
    "rainfall_mm_total",
]


class DataLogger:
    def __init__(self, filepath="data/sample_weather_data.csv"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writeheader()

    def log(self, reading: dict):
        """
        Appends a single reading (dict) to the CSV file.
        Missing keys are written as blank.
        """
        row = {"timestamp": datetime.now().isoformat(timespec="seconds")}
        row.update(reading)

        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writerow({k: row.get(k, "") for k in CSV_HEADERS})

    def read_all(self):
        """Returns all logged rows as a list of dicts."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, mode="r", newline="") as f:
            return list(csv.DictReader(f))


if __name__ == "__main__":
    logger = DataLogger()
    sample = {
        "temperature_c": 26.4,
        "humidity_percent": 58.2,
        "pressure_hpa": 1012.7,
        "probe_temperature_c": 25.9,
        "wind_speed_kmh": 8.3,
        "wind_direction": "NE",
        "rainfall_mm_total": 0.0,
    }
    logger.log(sample)
    print(f"Logged sample reading to {logger.filepath}")
