"""
wind_direction.py
-------------------
Interface module for a wind vane (potentiometer-based) read through
an MCP3008 8-channel ADC over SPI, since the Pi has no analog inputs.

Wiring (MCP3008 -> Pi, SPI0):
    VDD  -> 3.3V        CLK  -> GPIO11 (SCLK)
    VREF -> 3.3V        DOUT -> GPIO9  (MISO)
    AGND -> GND          DIN  -> GPIO10 (MOSI)
    CH0  -> Wind vane wiper    CS   -> GPIO8  (CE0)
    DGND -> GND

The wind vane outputs a variable resistance depending on direction,
mapped here to 8 compass points via voltage thresholds.
"""

import time

try:
    import busio
    import digitalio
    import board
    from adafruit_mcp3xxx.mcp3008 import MCP3008
    from adafruit_mcp3xxx.analog_in import AnalogIn
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError):
    HARDWARE_AVAILABLE = False

# Voltage ratio thresholds (Vout/Vin) mapped to compass directions.
# Calibrate against your specific wind vane's resistance table.
DIRECTION_TABLE = [
    (0.04, "N"), (0.13, "NE"), (0.28, "E"), (0.41, "SE"),
    (0.53, "S"), (0.68, "SW"), (0.82, "W"), (1.01, "NW"),
]


class WindDirectionSensor:
    def __init__(self):
        self.channel = None
        if HARDWARE_AVAILABLE:
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            cs = digitalio.DigitalInOut(board.D8)
            mcp = MCP3008(spi, cs)
            self.channel = AnalogIn(mcp, 0)  # CH0
        else:
            print("[wind_direction.py] Hardware not detected — running in simulation mode.")

    def _voltage_to_direction(self, ratio):
        for threshold, direction in DIRECTION_TABLE:
            if ratio <= threshold:
                return direction
        return "N"

    def read(self):
        """Returns dict: {wind_direction, raw_voltage}"""
        if self.channel:
            ratio = self.channel.voltage / 3.3
            direction = self._voltage_to_direction(ratio)
            return {"wind_direction": direction, "raw_voltage": round(self.channel.voltage, 3)}
        else:
            import random
            direction = random.choice([d for _, d in DIRECTION_TABLE])
            return {"wind_direction": direction, "raw_voltage": round(random.uniform(0, 3.3), 3)}


if __name__ == "__main__":
    sensor = WindDirectionSensor()
    while True:
        print(sensor.read())
        time.sleep(2)
