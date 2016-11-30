#!/usr/bin/env python

import time
import serial
import Queue

LEDS = 60

ser = serial.Serial( 
    port='/dev/ttyAMA0',
    baudrate = 57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

class Animations:

    stems = dict()

    def __init__(self, serial):
        self.serial = serial

    def add_steam(self, key, start_led, end_led, rgb):
        self.stems[key] = {
            'start_led': start_led,
            'end_led': end_led,
            'rgb': rgb
        }

    def attack(self, stem, rgb, delay):
        stem = self.stems[stem]
        stem_rgb = stem.get('rgb')
        start = stem.get('start_led')
        end = stem.get('end_led')

        for led in reversed(range(start, end)):
            print(led)
            # new color
            splixel = [led] + rgb
            ser.write(bytearray(splixel))
            time.sleep(delay)

            # back previous color
            splixel = [led] + stem_rgb
            ser.write(bytearray(splixel))
            time.sleep(delay)

anims = Animations(ser)

anims.add_steam('red', 14, 30, [0, 255, 0])

# base
for i in range(3):
    values = bytearray([i,250,250,250])
    ser.write(values)
    time.sleep(0.01)

while 1:

    anims.attack('red', [255, 0, 0], 0.1)
    time.sleep(0.01)

while 1:

    #for (anim in animations):
        #anim.render()

    # red
    for i in range(14,30):
        values = bytearray([i,250,0,0])
        ser.write(values)
        time.sleep(0.01)
    
    # green
    for i in range(30,43):
        values = bytearray([i,0,250,0])
        ser.write(values)
        time.sleep(0.01)
    
    # blue
    for i in range(43,60):
        values = bytearray([i,0,0,250])
        ser.write(values)
        time.sleep(0.01)
    
    for i in range(14,60):
        values = bytearray([i,0,0,0])
        ser.write(values)
        time.sleep(0.01)
    
