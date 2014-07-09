#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for some sensors"""

from __future__ import division, unicode_literals

import smbus


class ADT7410(object):
    """Class for ADT7410 connected to I2C bus

    :param bus: I2C bus number
    :param address: Device address of ADT7410
    """
    def __init__(self, bus, address=0x48):
        self._bus = smbus.SMBus(bus)
        self._address = address
        self._get_data()

    @property
    def resolution(self):
        """Resolution of the ADC

        0 = 13-bit resolution. Resolution of 0.0625 deg C
        1 = 16-bit resolution. Resolution of 0.0078 deg C
        """
        return self._get_bit(self._config, 7)

    @resolution.setter
    def resolution(self, value):
        self._set_config(self._set_bit(self._config, 7, value))

    @property
    def temperature(self):
        """Temperature in degrees (Celsius)"""
        self._get_data()
        if self.resolution == 0:
            temp = (self._temp_msb << 8 | self._temp_lsb) >> 3
            if temp >= 0x1000:
                temp -= 0x2000;
            return temp / 16
        else:
            temp = self._temp_msb << 8 | self._temp_lsb
            if temp >= 0x8000:
                temp -= 0x10000;
            return temp / 128

    def _get_bit(self, data, bit):
        return data >> bit & 1

    def _set_bit(self, data, bit, value):
        if value == 0:
            return data & 0 << bit
        elif value == 1:
            return data | 1 << bit
        else:
            raise ValueError
            return data

    def _get_data(self):
        """Get data from ADT7410"""
        data = map(int, self._bus.read_i2c_block_data(self._address, 0x00, 4))
        self._temp_msb = data[0x00]
        self._temp_lsb = data[0x01]
        self._status = data[0x02]
        self._config = data[0x03]

    def _set_config(self, value):
        """Set configuration bits"""
        self._bus.write_byte_data(self._address, 0x03, value)
        self._get_data()
