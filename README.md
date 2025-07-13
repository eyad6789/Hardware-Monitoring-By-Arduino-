# 🖥️ PC Hardware Monitor with Arduino TFT Display

This project monitors your PC hardware in real-time (CPU/GPU temperature, usage, RAM usage, FPS) and sends the data over serial to an Arduino, which displays it on a 2.4" ILI9341 TFT screen.

It features both simulated demo mode (Arduino-only) and real monitoring mode (Python script + PC data).

## 📦 Features
- ✅ Real-time hardware monitoring from your PC
- ✅ Displays CPU temp, GPU temp, CPU usage, RAM usage, GPU usage, and FPS
- ✅ Automatically detects and uses nvidia-smi, WMI, OpenHardwareMonitor, or LibreHardwareMonitor
- ✅ Serial communication between PC and Arduino
- ✅ Simulated demo mode without Python (Arduino only)
- ✅ Color-coded visual indicators and uptime display
- ✅ Robust error handling for missing sensors or disconnected ports

## 🖥️ PC (Python) Requirements
- Python 3.7+
- Libraries:
  - pyserial
  - psutil
  - wmi (optional, for better sensor access on Windows)

- Optional Tools:
  - NVIDIA GPU driver + nvidia-smi
  - OpenHardwareMonitor or LibreHardwareMonitor (for Windows sensor access)
Install required Python libraries:
```
pip install pyserial psutil
pip install wmi  
```
### 🔌 Arduino Setup
🧱 Hardware
- Arduino UNO or similar
- 2.4" ILI9341 TFT LCD (SPI Interface)

### 🔌 Wiring
| TFT Pin | Arduino Pin |
| ------- | ----------- |
| VCC     | 3.3V / 5V   |
| GND     | GND         |
| CS      | D10         |
| RST     | D9          |
| DC      | D8          |
| MOSI    | D11         |
| SCK     | D13         |
| LED     | 3.3V        |


## 📲 Arduino Libraries
- Adafruit GFX
- Adafruit ILI9341
- Install via Library Manager in Arduino IDE.

## 🚀 Getting Started
- Upload Arduino Sketch
- Open the provided Arduino sketch (.ino file)
- Upload it to your board
- Upon boot, the display shows either:
  - Demo Mode with simulated stats
  - "Waiting for PC data..." if ready for real-time mode
```
python monitor.py
```
- Enter the serial port (e.g., COM3 or /dev/ttyUSB0)
- Script will begin transmitting data every second
- Arduino will update screen in real time

## 🧠 Project Architecture
```
+--------------------+       Serial COM       +--------------------------+
|  Python Script     |  <------------------>  |     Arduino UNO + TFT    |
|  - Reads PC stats  |                       |  - Parses CSV data       |
|  - Formats data    |                       |  - Updates display        |
+--------------------+                       +--------------------------+
```
| Metric    | Range    | Source                                   |
| --------- | -------- | ---------------------------------------- |
| CPU Temp  | 0–100 °C | psutil / WMI / OpenHardwareMonitor       |
| GPU Temp  | 0–100 °C | `nvidia-smi` / WMI / OpenHardwareMonitor |
| CPU Usage | 0–100 %  | psutil                                   |
| RAM Usage | 0–100 %  | psutil                                   |
| GPU Usage | 0–100 %  | `nvidia-smi` / OpenHardwareMonitor       |
| FPS       | 30–144   | Estimated or read via sensors            |
Color-coded performance bars and categories (LOW, OK, GOOD, HIGH) are displayed.

## ⚙️ Advanced Notes
- The Arduino sketch supports simulated mode if no PC is connected.
- The Python script falls back to simulated values if hardware sensors aren't available.
- Data is sent as CSV over serial:
```
CPU_Temp,GPU_Temp,CPU_Usage,RAM_Usage,GPU_Usage,FPS
```
## 🛠️ Troubleshooting
| Issue                       | Solution                                |
| --------------------------- | --------------------------------------- |
| `SerialException` on Python | Make sure the correct COM port is used  |
| Arduino shows "Waiting..."  | Ensure Python is running and port is OK |
| Missing `nvidia-smi` output | Install NVIDIA drivers and CLI tools    |
| No temperature readings     | Install WMI or use LibreHardwareMonitor |

## 📁 File Structure
```
├── monitor.py                # Python script for data collection
├── arduino_tft_monitor.ino  # Arduino sketch for TFT display
└── README.md                 # This file
```
## 📷 Demo Preview
🖼️ (You can include a GIF or image of the live monitor if available)

🤝 Credits
Created by: [Eyad Qasim]
- Libraries Used:
- Adafruit GFX
- Adafruit ILI9341
- psutil
- pyserial
- OpenHardwareMonitor
- LibreHardwareMonitor

## 📜 License
MIT License - use freely with attribution

## Author
Developed by "Eyad Qasim Raheem" 
[LinkedIn Profile](https://www.linkedin.com/in/eyad-qasim-2a96b624b/)

[GitHub Profile](https://github.com/eyad6789)

