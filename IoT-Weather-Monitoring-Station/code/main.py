"""
main.py
--------
Entry point for the IoT-Based Weather Monitoring Station.

Polls all sensors on a fixed interval, merges their readings into a
single record, prints it to console, and logs it to CSV via
data_logger.py.

Usage:
    python3 main.py                # run continuously (Ctrl+C to stop)
    python3 main.py --once         # take a single reading and exit
    python3 main.py --interval 10  # set polling interval in seconds
"""

import argparse
import time
import sys

from bme280 import BME280Sensor
from ds18b20 import DS18B20Sensor
from wind_speed import WindSpeedSensor
from wind_direction import WindDirectionSensor
from rainfall import RainfallSensor
from data_logger import DataLogger


def parse_args():
    parser = argparse.ArgumentParser(description="IoT Weather Monitoring Station")
    parser.add_argument("--interval", type=int, default=60,
                         help="Seconds between readings (default: 60)")
    parser.add_argument("--once", action="store_true",
                         help="Take a single reading and exit")
    parser.add_argument("--csv", type=str, default="data/sample_weather_data.csv",
                         help="Path to output CSV file")
    return parser.parse_args()


def collect_reading(bme280, ds18b20, wind_speed, wind_direction, rainfall):
    """Polls all sensors and merges results into one dict."""
    reading = {}

    for result in [
        bme280.read(),
        ds18b20.read(),
        wind_speed.read(),
        wind_direction.read(),
        rainfall.read(),
    ]:
        if result:
            reading.update(result)

    return reading


def format_reading(reading: dict) -> str:
    return (
        f"🌡  Temp: {reading.get('temperature_c', '—')}°C "
        f"(probe: {reading.get('probe_temperature_c', '—')}°C) | "
        f"💧 Humidity: {reading.get('humidity_percent', '—')}% | "
        f"📈 Pressure: {reading.get('pressure_hpa', '—')} hPa | "
        f"🌬 Wind: {reading.get('wind_speed_kmh', '—')} km/h "
        f"({reading.get('wind_direction', '—')}) | "
        f"🌧 Rain: {reading.get('rainfall_mm_total', '—')} mm"
    )


def main():
    args = parse_args()

    print("Initializing sensors...")
    bme280 = BME280Sensor()
    ds18b20 = DS18B20Sensor()
    wind_speed = WindSpeedSensor()
    wind_direction = WindDirectionSensor()
    rainfall = RainfallSensor()
    logger = DataLogger(filepath=args.csv)

    print(f"Weather station running (interval={args.interval}s). Press Ctrl+C to stop.\n")

    try:
        while True:
            reading = collect_reading(bme280, ds18b20, wind_speed, wind_direction, rainfall)
            print(format_reading(reading))
            logger.log(reading)

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nShutting down weather station...")
    finally:
        wind_speed.cleanup()
        rainfall.cleanup()
        print("Cleanup complete. Data saved to", args.csv)
        sys.exit(0)


if __name__ == "__main__":
    main()
