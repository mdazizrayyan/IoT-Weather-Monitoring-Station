"""
rainfall.py
------------
Interface module for a tipping-bucket rain gauge.
Each "tip" closes a reed switch momentarily, corresponding to a fixed
volume of rainfall (commonly 0.2794 mm or 0.011 in per tip — check
your gauge's datasheet).

Wiring:
    Signal -> GPIO17 (Pin 11), pulled up internally
    GND    -> GND
"""

import time

try:
    import RPi.GPIO as GPIO
    HARDWARE_AVAILABLE = True
except (ImportError, RuntimeError):
    HARDWARE_AVAILABLE = False

RAIN_PIN = 17
MM_PER_TIP = 0.2794  # calibrate to your rain gauge's datasheet


class RainfallSensor:
    def __init__(self, pin=RAIN_PIN):
        self.pin = pin
        self._tip_count = 0
        self._total_mm = 0.0

        if HARDWARE_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._tip_callback, bouncetime=200)
        else:
            print("[rainfall.py] Hardware not detected — running in simulation mode.")

    def _tip_callback(self, channel):
        self._tip_count += 1
        self._total_mm += MM_PER_TIP

    def read(self):
        """Returns dict: {rainfall_mm_total, tip_count}"""
        if HARDWARE_AVAILABLE:
            return {"rainfall_mm_total": round(self._total_mm, 3), "tip_count": self._tip_count}
        else:
            import random
            # simulate occasional light rain
            if random.random() < 0.1:
                self._tip_count += 1
                self._total_mm += MM_PER_TIP
            return {"rainfall_mm_total": round(self._total_mm, 3), "tip_count": self._tip_count}

    def reset(self):
        """Reset accumulated rainfall (e.g. at midnight for daily totals)."""
        self._tip_count = 0
        self._total_mm = 0.0

    def cleanup(self):
        if HARDWARE_AVAILABLE:
            GPIO.remove_event_detect(self.pin)


if __name__ == "__main__":
    sensor = RainfallSensor()
    try:
        while True:
            print(sensor.read())
            time.sleep(2)
    except KeyboardInterrupt:
        sensor.cleanup()
