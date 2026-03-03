# wipy-screen

Test script for a **0.96" SSD1306 I2C OLED display** connected to a **Pycom WiPy** (MicroPython).

## Display Specs

| Property   | Value          |
|------------|----------------|
| Driver     | SSD1306        |
| Size       | 0.96 inch      |
| Resolution | 128 × 64 px    |
| Interface  | I2C            |
| Color      | Monochrome     |
| Voltage    | 3.3V           |

## Wiring

```
    WiPy                    OLED 0.96"
  ┌────────┐              ┌──────────┐
  │   3.3V ├──────────────┤ VCC      │
  │    GND ├──────────────┤ GND      │
  │     P9 ├──────────────┤ SDA      │
  │    P10 ├──────────────┤ SCL      │
  └────────┘              └──────────┘
```

No external resistors needed — the OLED module has pull-ups built in.

## What the test does

1. Scans the I2C bus and prints detected devices
2. Displays screen info (driver, resolution, pixel count)
3. Runs visual tests: fill, border, checkerboard, diagonals
4. Scrolling text animation
5. Ends showing screen info again

## Setup

### 1. Install serial driver (Windows)

The WiPy uses a CP210x USB-to-serial chip. Install the driver from [Silicon Labs](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) if your OS doesn't recognize it automatically.

After plugging in, check **Device Manager** → **Ports (COM & LPT)** for the assigned COM port (e.g. `COM3`).

### 2. Get the SSD1306 library

Download `ssd1306.py` from the [micropython-lib repo](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py) and place it alongside `main.py`.

### 3. Flash files to the WiPy

#### Option A: Pymakr (VS Code)

1. Install the **Pymakr** extension in VS Code
2. Open this project folder
3. Connect WiPy via USB
4. Pymakr should detect the board — set the COM port if needed
5. Click **Upload** to sync all files to the board
6. The board resets and runs `main.py` automatically

#### Option B: ampy (CLI)

It is recommended to use a virtual environment to avoid conflicts with system packages.

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install ampy
pip install adafruit-ampy

# Upload files (replace COM3 with your port)
ampy --port COM3 put ssd1306.py
ampy --port COM3 put boot.py
ampy --port COM3 put main.py

# Reset the board or run directly
ampy --port COM3 run main.py

# Deactivate when done
deactivate
```

> **Windows tip:** If `python` is not found, try `py -m venv venv` instead.

#### Option C: rshell

It is recommended to use a virtual environment to avoid conflicts with system packages.

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install rshell
pip install rshell

# Connect and copy files (replace COM3 with your port)
rshell --port COM3

# Inside rshell prompt:
cp ssd1306.py /pyboard/
cp boot.py /pyboard/
cp main.py /pyboard/
repl   # open REPL to see output (Ctrl+X to exit)

# Deactivate when done
deactivate
```

> **Windows tip:** rshell may require `--buffer-size 512` if you get timeouts:
> `rshell --port COM3 --buffer-size 512`

### 4. Serial monitor

To see print output, connect to the REPL at **115200 baud**:

- **PuTTY** (Windows): Serial, COM3, 115200
- **VS Code**: Pymakr terminal
- **CLI**: `screen /dev/ttyUSB0 115200` (Linux/Mac)

## Firmware updates

If you need to update the WiPy's MicroPython firmware, use the [Pycom Firmware Updater](https://docs.pycom.io/updatefirmware/device/).

> **Note:** Pycom ceased operations in ~2022. Tools and firmware still work but are community-maintained.

## License

MIT
