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


class LPS331(object):
    """Class for LPS331 connected to I2C bus

    :param bus: I2C bus number
    :param address: Device address of LPS331
    """
    def __init__(self, bus, address=0x5d):
        self._bus = smbus.SMBus(bus)
        self._address = address
        self.who_am_i()

    def who_am_i(self):
        data = int(self._bus.read_byte_data(self._address, 0x0f))
        if data != 0xbb:
            self.close()
            raise Exception("Device error")

    def open(self):
        # Activate
        self._bus.write_byte_data(self._address, 0x20, 0x90);

    def close(self):
        # Close
        self._bus.write_byte_data(self._address, 0x20, 0x00);

    @property
    def pressure(self):
        """Pressure in hPa"""
        self._bus.write_byte_data(self._address, 0x21, 0x01)
        while True:
            status = self._bus.read_byte_data(self._address, 0x27)
            if status & 0x02:
                break
        pressure_xl = self._bus.read_byte_data(self._address, 0x28)
        pressure_l = self._bus.read_byte_data(self._address, 0x29)
        pressure_h = self._bus.read_byte_data(self._address, 0x2a)
        counts = ((pressure_h << 16) | (pressure_l << 8) | pressure_xl)
        if counts & 0x800000 == 0x800000:
            counts = -((counts ^ 0xffffff) + 0x1)
        hpa = counts / 4096
        return hpa

    @property
    def temperature(self):
        """Temperature in degrees (Celsius)"""
        self._bus.write_byte_data(self._address, 0x21, 0x01)
        while True:
            status = self._bus.read_byte_data(self._address, 0x27)
            if status & 0x01:
                break
        temp_h = self._bus.read_byte_data(self._address, 0x2c)
        temp_l = self._bus.read_byte_data(self._address, 0x2b)
        counts = (temp_h << 8) | temp_l
        if counts & 0x8000 == 0x8000:
            counts = -((counts ^ 0xffff) + 0x1)
        temp = 42.5 + (counts / 480)
        return temp
