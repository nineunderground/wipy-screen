"""
WiPy OLED Screen Test
Tests a 0.96" SSD1306 I2C OLED display connected to a Pycom WiPy.
Displays screen info and runs a pixel test pattern.
"""

import time
from machine import I2C, Pin
import ssd1306


def get_screen_info(oled):
    """Return display details as a dict."""
    return {
        "driver": "SSD1306",
        "interface": "I2C",
        "width": oled.width,
        "height": oled.height,
        "pixels": oled.width * oled.height,
        "color": "Monochrome",
        "size": '0.96"',
    }


def show_info(oled, info):
    """Display screen details on the OLED."""
    oled.fill(0)
    oled.text("== Screen Info ==", 0, 0)
    oled.text("Driver: {}".format(info["driver"]), 0, 12)
    oled.text("Res: {}x{}".format(info["width"], info["height"]), 0, 22)
    oled.text("Pixels: {}".format(info["pixels"]), 0, 32)
    oled.text("Color: {}".format(info["color"]), 0, 42)
    oled.text("Size: {}".format(info["size"]), 0, 52)
    oled.show()


def test_fill(oled):
    """Fill screen white, then black."""
    oled.fill(1)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.show()
    time.sleep(0.5)


def test_border(oled):
    """Draw a border rectangle."""
    oled.fill(0)
    w, h = oled.width, oled.height
    for x in range(w):
        oled.pixel(x, 0, 1)
        oled.pixel(x, h - 1, 1)
    for y in range(h):
        oled.pixel(0, y, 1)
        oled.pixel(w - 1, y, 1)
    oled.text("Border Test", 20, 28)
    oled.show()


def test_checkerboard(oled, size=8):
    """Draw a checkerboard pattern."""
    oled.fill(0)
    for y in range(oled.height):
        for x in range(oled.width):
            if (x // size + y // size) % 2:
                oled.pixel(x, y, 1)
    oled.show()


def test_diagonal(oled):
    """Draw diagonal lines."""
    oled.fill(0)
    for i in range(min(oled.width, oled.height)):
        oled.pixel(i, i, 1)
        oled.pixel(oled.width - 1 - i, i, 1)
    oled.text("Diagonal", 32, 28)
    oled.show()


def test_scrolling_text(oled, text="WiPy + SSD1306 OLED Test "):
    """Scroll text across the screen."""
    for offset in range(len(text) * 8):
        oled.fill(0)
        oled.text(text, -offset, 28)
        oled.show()
        time.sleep(0.05)


def scan_i2c(i2c):
    """Scan and print I2C devices found."""
    devices = i2c.scan()
    print("I2C scan found {} device(s):".format(len(devices)))
    for d in devices:
        print("  - 0x{:02X} ({})".format(d, d))
    return devices


def main():
    print("Initializing I2C...")
    i2c = I2C(0, pins=('P9', 'P10'))

    devices = scan_i2c(i2c)
    if not devices:
        print("ERROR: No I2C devices found. Check wiring.")
        return

    print("Initializing SSD1306 OLED (128x64)...")
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    info = get_screen_info(oled)
    print("Screen info:")
    for k, v in info.items():
        print("  {}: {}".format(k, v))

    print("\n[1/5] Showing screen info...")
    show_info(oled, info)
    time.sleep(3)

    print("[2/5] Fill test...")
    test_fill(oled)
    time.sleep(1)

    print("[3/5] Border test...")
    test_border(oled)
    time.sleep(2)

    print("[4/5] Checkerboard test...")
    test_checkerboard(oled)
    time.sleep(2)

    print("[5/5] Diagonal test...")
    test_diagonal(oled)
    time.sleep(2)

    print("\nScrolling text...")
    test_scrolling_text(oled)

    # End with screen info
    show_info(oled, info)
    print("\nAll tests complete!")


if __name__ == "__main__":
    main()
