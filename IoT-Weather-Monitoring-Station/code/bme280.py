"""
bme280.py
----------
Interface module for the BME280 sensor (Temperature, Humidity, Pressure).
Communicates over I2C using the smbus2 / adafruit_bme280 libraries.

Wiring (I2C):
    VIN  -> 3.3V (Pi Pin 1)
    GND  -> GND  (Pi Pin 6)
    SCL  -> SCL  (Pi Pin 5, GPIO3)
    SDA  -> SDA  (Pi Pin 3, GPIO2)
"""

import time

try:
    import board
    import busio
    import adafruit_bme280.advanced as adafruit_bme280
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError):
    HARDWARE_AVAILABLE = False


class BME280Sensor:
    """Wrapper class for reading temperature, humidity, and pressure."""

    def __init__(self, address=0x76):
        self.address = address
        self.sensor = None

        if HARDWARE_AVAILABLE:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=self.address)
            self.sensor.sea_level_pressure = 1013.25
            self.sensor.mode = adafruit_bme280.MODE_NORMAL
            self.sensor.standby_period = adafruit_bme280.STANDBY_TC_500
            self.sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
            self.sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
            self.sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
            self.sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2
        else:
            print("[bme280.py] Hardware not detected — running in simulation mode.")

    def read(self):
        """
        Returns a dict: {temperature_c, humidity_percent, pressure_hpa}
        Falls back to simulated values if hardware is unavailable.
        """
        if self.sensor:
            try:
                return {
                    "temperature_c": round(self.sensor.temperature, 2),
                    "humidity_percent": round(self.sensor.relative_humidity, 2),
                    "pressure_hpa": round(self.sensor.pressure, 2),
                }
            except Exception as e:
                print(f"[bme280.py] Read error: {e}")
                return None
        else:
            import random
            return {
                "temperature_c": round(25 + random.uniform(-2, 2), 2),
                "humidity_percent": round(55 + random.uniform(-5, 5), 2),
                "pressure_hpa": round(1013 + random.uniform(-3, 3), 2),
            }


if __name__ == "__main__":
    sensor = BME280Sensor()
    while True:
        data = sensor.read()
        print(data)
        time.sleep(2)
