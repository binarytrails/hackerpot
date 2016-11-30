#!/usr/bin/env python

import time
import serial

LEDS = 17

ser = serial.Serial( 
    port='/dev/ttyAMA0',
    baudrate = 57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:

#    try:
#        data = ser.read()
#        print("Serial read: %s" % data)
#    except:
#        pass

    # fastest .sleep of 0.01

    #try:
        for i in range(LEDS):
            values = bytearray([i,200,0,0])
            ser.write(values)
            time.sleep(0.01)
        
            values = bytearray([i,0,0,0])
            ser.write(values)
    
    #except (KeyboardInterrupt):                # more hard to stop
    #    for i in range(LEDS):
    #        values = bytearray([i,0,0,0])
    #        ser.write(values)
    #        time.sleep(0.01)
               
