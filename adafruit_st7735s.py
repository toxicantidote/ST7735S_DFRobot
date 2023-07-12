# SPDX-FileCopyrightText: 2019 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_st7735s`
====================================================

Displayio driver for ST7735S based displays.

* Author(s): Scott Shawcroft and Melissa LeBlanc-Williams
Modified by Toxicantidote to suit ST7735S based displays

Implementation Notes
--------------------

**Hardware:**

ST7735S based displays.

Tested with the DFRobot 1.8in TFT display (SKU: DFR0928)
<https://wiki.dfrobot.com/SKU_DFR0928_Fermion_1.8_Inches_128_160_IPS_TFT_LCD_Display_with_MicroSD_Card_Slot_Breakout>

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""
try:
    # used for typing only
    from typing import Any
except ImportError:
    pass

import displayio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ST7735R.git"

_INIT_SEQUENCE = bytearray(
    b"\x01\x11\x80\x78"  # Exit sleep and Delay 150ms  
    b"\xb1\x03\x01\x2C\x2D"  # Frame rate control (normal mode)
    b"\xb2\x03\x01\x2C\x2D"  # Frame rate control (idle mode)
    b"\xb3\x06\x01\x2C\x2D\x01\x2C\x2D"  # Frame rate control (local mode)
    b"\xb4\x01\x07"  # Reverse control
    b"\xb6\x03\xA2\x02\x84"  # Frame rate control (idle mode)  
    b"\xc0\x03\xa2\x02\x84"  # _PWCTR1 GVDD = 4.7V, 1.0uA
    b"\xc1\x01\xc5"  # _PWCTR2 VGH=14.7V, VGL=-7.35V
    b"\xc2\x02\x0a\x00"  # _PWCTR3 Opamp current small, Boost frequency
    b"\xc3\x02\x8a\x2a" # More power consumption control
    b"\xc4\x02\x8a\xee" # More power consumption control
    b"\xc5\x01\x0e"  # _VMCTR1 VCOMH = 4V, VOML = -1.1V
    b"\x20\x00"  # _INVOFF
    b"\x3a\x01\x05" # Colour mode setting (16 bit)
    b"\x36\x01\xc0"  # _MADCTL bottom to top refresh
    b"\x2a\x04\x00\x00\x00\x4f" # Memory data access control commands
    b"\x2b\x04\x00\x00\x00\x9f" # Memory data access control commands
    b"\xe0\x10\x04\x22\x07\x0a\x2e\x30\x25\x2a\x28\x26\x2e\x3a\x00\x01\x03\x13"  # _GMCTRP1 Gamma
    b"\xe1\x10\x04\x16\x06\x0d\x2d\x26\x23\x27\x27\x25\x2d\x3b\x00\x01\x04\x13"  # _GMCTRN1
    b"\x01\x29\x00\x00"
)


# pylint: disable=too-few-public-methods
class ST7735S(displayio.Display):
    """
    ST7735S display driver

    :param displayio.FourWire bus: bus that the display is connected to
    :param bool bgr: (Optional) An extra init sequence to append (default=False)
    :param bool invert: (Optional) Invert the colors (default=False)
    """

    def __init__(
        self,
        bus: displayio.FourWire,
        *,
        bgr: bool = False,
        invert: bool = False,
        **kwargs: Any
    ):
        init_sequence = _INIT_SEQUENCE
        if bgr:
            init_sequence += (
                b"\x36\x01\xC0"  # _MADCTL Default rotation plus BGR encoding
            )
        else:
            init_sequence += (
                b"\x36\x01\xC8"  # _MADCTL Default rotation plus RGB encoding
            )
        if invert:
            init_sequence += b"\x21\x00"  # _INVON
        super().__init__(bus, init_sequence, **kwargs)
