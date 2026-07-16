# 🌦️ IoT-Based Weather Monitoring Station Using Raspberry Pi

An IoT-based Weather Monitoring Station developed using **Raspberry Pi** to monitor environmental conditions in real time. The system collects weather parameters such as temperature, humidity, atmospheric pressure, wind speed, wind direction, and rainfall using multiple sensors and processes the data using Python.

---

## 📖 Overview

Weather monitoring plays an important role in agriculture, environmental research, disaster management, and smart city applications. This project demonstrates a low-cost and scalable IoT solution that continuously collects environmental data through multiple sensors connected to a Raspberry Pi.

---

## 🎯 Objectives

- Develop an IoT-based weather monitoring system.
- Monitor real-time weather conditions.
- Interface multiple environmental sensors with Raspberry Pi.
- Process sensor data using Python.
- Store collected data for future analysis.
- Build a scalable weather monitoring solution.

---

## 🛠️ Hardware Components

| Component | Purpose |
|---|---|
| Raspberry Pi (3B+ / 4) | Main processing unit |
| BME280 Sensor | Temperature, humidity, pressure (I2C) |
| DS18B20 Temperature Sensor | Secondary/probe temperature (1-Wire) |
| Anemometer (Wind Speed Sensor) | Wind speed via pulse counting |
| Wind Vane (Wind Direction Sensor) | Wind direction via analog voltage |
| Rain Gauge | Rainfall via tipping-bucket pulses |
| MCP3008 ADC | Analog-to-digital conversion for wind vane |
| Breadboard | Prototyping |
| Jumper Wires | Connections |
| Power Supply | 5V/3A USB-C for Raspberry Pi |

See [`diagrams/circuit_diagram.png`](diagrams/circuit_diagram.png) for full wiring.

---

## 💻 Software Requirements

- Raspberry Pi OS (Bullseye or later, with I2C/SPI/1-Wire enabled via `raspi-config`)
- Python 3.9+
- Visual Studio Code (or any editor, for development)
- GPIO Libraries (`RPi.GPIO`)
- `smbus2`
- Adafruit Blinka + CircuitPython sensor libraries

Install everything with:

```bash
pip install -r requirements.txt
```

> **Note:** On non-Raspberry Pi machines (e.g. for development/testing), all sensor modules automatically fall back to **simulation mode** and generate realistic random values, so the full pipeline runs and can be tested without hardware.

---

## 📂 Project Structure

```text
IoT-Weather-Monitoring-Station/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── code/
│   ├── main.py
│   ├── bme280.py
│   ├── ds18b20.py
│   ├── wind_speed.py
│   ├── wind_direction.py
│   ├── rainfall.py
│   └── data_logger.py
│
├── diagrams/
│   ├── system_architecture.png / .svg
│   ├── circuit_diagram.png / .svg
│   └── flowchart.png / .svg
│
├── images/
│   ├── hardware_setup.jpg
│   ├── prototype.jpg
│   └── dashboard.png
│
├── data/
│   └── sample_weather_data.csv
│
├── report/
│   └── Internship_Report.pdf
│
└── presentation/
    └── Internship_Presentation.pptx
```

---

## ⚙️ Working Principle

1. Environmental sensors collect weather data (temperature, humidity, pressure, wind speed/direction, rainfall).
2. Raspberry Pi polls each sensor over its respective interface (I2C, 1-Wire, GPIO, SPI).
3. `main.py` merges all readings into a single timestamped record and processes the data.
4. Weather information is stored locally as CSV via `data_logger.py`.
5. Data is printed to console for live monitoring and saved for later analysis.

See [`diagrams/flowchart.png`](diagrams/flowchart.png) for the full logic flow and [`diagrams/system_architecture.png`](diagrams/system_architecture.png) for the system-level view.

---

## ▶️ Running the Project

```bash
cd code

# Single reading, printed and logged, then exit
python3 main.py --once

# Continuous monitoring every 60 seconds (default)
python3 main.py

# Continuous monitoring with a custom interval (e.g. every 10s)
python3 main.py --interval 10

# Log to a custom CSV path
python3 main.py --csv ../data/sample_weather_data.csv
```

Sample console output:
```
🌡  Temp: 24.88°C (probe: 25.11°C) | 💧 Humidity: 55.94% | 📈 Pressure: 1016.0 hPa | 🌬 Wind: 12.85 km/h (SE) | 🌧 Rain: 0.0 mm
```

---

## 📊 Parameters Monitored

- 🌡 Temperature
- 💧 Humidity
- 🌬 Wind Speed
- 🧭 Wind Direction
- 🌧 Rainfall
- 📈 Atmospheric Pressure

---

## 🚀 Applications

- Smart Agriculture
- Environmental Monitoring
- Smart Cities
- Educational Projects
- Weather Observation
- Research Laboratories

---

## ✅ Features

- Real-time weather monitoring
- Raspberry Pi-based implementation
- Python programming
- Modular sensor integration
- Low-cost solution
- Easy to expand
- Data logging support
- Simulation mode for development without physical hardware

---

## 🔮 Future Enhancements

- Cloud Integration
- Mobile Application
- AI-based Weather Prediction
- Air Quality Monitoring
- Solar Powered Weather Station
- Real-time Dashboard

---

## 👨‍💻 Developed By

**Aziz Rayyan**
B.Tech Computer Engineering (AI & ML)
Presidency University, Bengaluru
Samsung Innovation Campus – Summer Internship 2026

---

## 📚 References

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Python Documentation](https://docs.python.org/3/)
- [BME280 Datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/)
- [DS18B20 Datasheet](https://www.analog.com/en/products/ds18b20.html)
- [Bosch Sensortec Documentation](https://www.bosch-sensortec.com/)

---

## 📜 License

This project is developed for academic and educational purposes as part of the Samsung Innovation Campus Summer Internship 2026. See [LICENSE](LICENSE) for details.
