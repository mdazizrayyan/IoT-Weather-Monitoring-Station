"""
wind_speed.py
--------------
Interface module for a cup-type anemometer (reed switch based).
Each rotation closes the reed switch once; wind speed is derived from
pulse frequency over a fixed sampling window.

Wiring:
    Signal -> GPIO27 (Pin 13), pulled up internally
    GND    -> GND

Calibration:
    Standard anemometers: 1 rotation/sec ≈ 2.4 km/h (adjust CAL_FACTOR
    to match your specific anemometer's datasheet).
"""

import time

try:
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except (ImportError, RuntimeError):
    HARDWARE_AVAILABLE = False

WIND_SPEED_PIN = 27
CAL_FACTOR = 2.4  # km/h per rotation/sec — adjust per anemometer datasheet


class WindSpeedSensor:
    def __init__(self, pin=WIND_SPEED_PIN, sample_seconds=3):
        self.pin = pin
        self.sample_seconds = sample_seconds
        self._pulse_count = 0

        if HARDWARE_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._pulse_callback)
        else:
            print("[wind_speed.py] Hardware not detected — running in simulation mode.")

    def _pulse_callback(self, channel):
        self._pulse_count += 1

    def read(self):
        """
        Samples pulses over `sample_seconds` and returns wind speed in km/h.
        Returns dict: {wind_speed_kmh}
        """
        if HARDWARE_AVAILABLE:
            self._pulse_count = 0
            time.sleep(self.sample_seconds)
            rotations_per_sec = self._pulse_count / self.sample_seconds
            speed_kmh = round(rotations_per_sec * CAL_FACTOR, 2)
            return {"wind_speed_kmh": speed_kmh}
        else:
            import random
            time.sleep(0.1)
            return {"wind_speed_kmh": round(random.uniform(0, 20), 2)}

    def cleanup(self):
        if HARDWARE_AVAILABLE:
            GPIO.remove_event_detect(self.pin)


if __name__ == "__main__":
    sensor = WindSpeedSensor()
    try:
        while True:
            print(sensor.read())
    except KeyboardInterrupt:
        sensor.cleanup()
