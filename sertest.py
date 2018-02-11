#!/usr/bin/env python

import serial

ser = serial.Serial('/dev/ttyUSB0', timeout=5)

line = ser.readline().strip()

print line

ser.close()
