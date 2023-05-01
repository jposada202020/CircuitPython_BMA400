# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`bma400`
================================================================================

BMA400 Bosch Accelerometer CircuitPython Driver


* Author(s): Jose D. Montoya


"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct
from adafruit_register.i2c_bits import RWBits

# from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct

try:
    from busio import I2C
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_BMA400.git"


_REG_WHOAMI = const(0x90)
_ACC_CONFIG0 = const(0x19)

# Power Modes
SLEEP_MODE = const(0x00)
LOW_POWER_MODE = const(0x01)
NORMAL_MODE = const(0x02)
SWITCH_TO_SLEEP = const(0x03)
power_mode_values = (SLEEP_MODE, LOW_POWER_MODE, NORMAL_MODE, SWITCH_TO_SLEEP)

# pylint: disable=too-few-public-methods
class BMA400:
    """Driver for the BMA400 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the BMA400 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x14`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`BMA400` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import bma400

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        bma = bma400.BMA400(i2c)

    Now you have access to the attributes

    .. code-block:: python

        accx, accy, accz = bma.acceleration

    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")

    # ACC_CONFIG0 (0x19)
    # | filt1_bw | osr_lp(1) | osr_lp(0) | ---- | ---- | ---- | power_mode(1) | power_mode(0) |
    _power_mode = RWBits(2, _ACC_CONFIG0, 0)

    def __init__(self, i2c_bus: I2C, address: int = 0x14) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0x90:
            raise RuntimeError("Failed to find BMA400")

    @property
    def power_mode(self) -> str:
        """
        Sensor power_mode

        +------------------------------------+------------------+
        | Mode                               | Value            |
        +====================================+==================+
        | :py:const:`bma400.SLEEP_MODE`      | :py:const:`0x00` |
        +------------------------------------+------------------+
        | :py:const:`bma400.LOW_POWER_MODE`  | :py:const:`0x01` |
        +------------------------------------+------------------+
        | :py:const:`bma400.NORMAL_MODE`     | :py:const:`0x02` |
        +------------------------------------+------------------+
        | :py:const:`bma400.SWITCH_TO_SLEEP` | :py:const:`0x03` |
        +------------------------------------+------------------+
        """
        values = (
            "SLEEP_MODE",
            "LOW_POWER_MODE",
            "NORMAL_MODE",
            "SWITCH_TO_SLEEP",
        )
        return values[self._power_mode]

    @power_mode.setter
    def power_mode(self, value: int) -> None:
        if value not in power_mode_values:
            raise ValueError("Value must be a valid power_mode setting")
        self._power_mode = value
