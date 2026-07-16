"""
ds18b20.py
-----------
Interface module for the DS18B20 1-Wire digital temperature sensor.
Used as a secondary/outdoor temperature probe alongside the BME280.

Wiring (1-Wire):
    VDD  -> 3.3V
    GND  -> GND
    DATA -> GPIO4 (Pin 7) with a 4.7k pull-up resistor to 3.3V

Requires 1-Wire interface enabled in /boot/config.txt:
    dtoverlay=w1-gpio
"""

import time

try:
    from w1thermsensor import W1ThermSensor, NoSensorFoundError
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False


class DS18B20Sensor:
    """Wrapper class for reading the DS18B20 probe temperature."""

    def __init__(self):
        self.sensor = None
        if HARDWARE_AVAILABLE:
            try:
                self.sensor = W1ThermSensor()
            except NoSensorFoundError:
                print("[ds18b20.py] No DS18B20 sensor found — running in simulation mode.")
        else:
            print("[ds18b20.py] Hardware not detected — running in simulation mode.")

    def read(self):
        """Returns dict: {probe_temperature_c}"""
        if self.sensor:
            try:
                temp_c = self.sensor.get_temperature()
                return {"probe_temperature_c": round(temp_c, 2)}
            except Exception as e:
                print(f"[ds18b20.py] Read error: {e}")
                return None
        else:
            import random
            return {"probe_temperature_c": round(24 + random.uniform(-2, 2), 2)}


if __name__ == "__main__":
    sensor = DS18B20Sensor()
    while True:
        print(sensor.read())
        time.sleep(2)
