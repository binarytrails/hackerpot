#!/usr/bin/env python

import time
import serial

LEDS = 60

ser = serial.Serial( 
    port='/dev/ttyAMA0',
    baudrate = 57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

for i in range(3):
    values = bytearray([i,250,250,250])
    ser.write(values)
    time.sleep(0.01)

while 1:

    for i in range(14,30):
        values = bytearray([i,250,0,0])
        ser.write(values)
        time.sleep(0.01)
    
    for i in range(30,43):
        values = bytearray([i,0,250,0])
        ser.write(values)
        time.sleep(0.01)
    
    for i in range(43,60):
        values = bytearray([i,0,0,250])
        ser.write(values)
        time.sleep(0.01)
    
    for i in range(14,60):
        values = bytearray([i,0,0,0])
        ser.write(values)
        time.sleep(0.01)
    
