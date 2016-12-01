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

class HackerPotAnimations:

    pot = dict()
    stems = dict()

    def __init__(self, serial, max_leds):
        self.SERIAL = serial
        self.MAX_LEDS = max_leds 

    def init_pot(self, start_led, end_led, rgb):
        self.pot = {
            'start_led': start_led,
            'end_led': end_led,
            'rgb': rgb
        }

    def add_steam(self, key, start_led, end_led, rgb):
        self.stems[key] = {
            'start_led': start_led,
            'end_led': end_led,
            'rgb': rgb
        }

    def recolorize(self, delay):
        self.colorize(self.pot['rgb'], delay)
    
    def colorize(self, rgb, delay):
        for led in range(self.MAX_LEDS):
            self.SERIAL.write(bytearray([led] + rgb))
            time.sleep(delay)

    def animate_attack(self, key, rgb, delay):
        stem = self.stems[key]
        stem_rgb = stem.get('rgb')
        start = stem.get('start_led')
        end = stem.get('end_led')

        for led in reversed(range(start, end)):
            # new color
            splixel = [led] + rgb
            ser.write(bytearray(splixel))
            time.sleep(delay)

            # back previous color
            splixel = [led] + stem_rgb
            self.SERIAL.write(bytearray(splixel))
            time.sleep(delay)

        # influence stem color
        for i in range(len(rgb)):
            # by 1 / 10 of attack color
            new_rgb = stem_rgb[i] + int(rgb[i] / 10)
            
            if new_rgb > 255:
                new_rgb = 255

            self.stems[key]['rgb'][i] = new_rgb

anims = HackerPotAnimations(ser, 60)

base_color = [0, 255, 0]
anims.init_pot(0, 14, base_color)
anims.recolorize(0.01)

anims.add_steam('r', 14, 30, base_color)
anims.add_steam('w', 30, 43, base_color)
anims.add_steam('b', 43, 60, base_color)

# everything
while 1:

    anims.animate_attack('r', [255, 0, 0], 0.01)
    #anims.animate_attack('w', [255, 255, 255], 0.1)
    #anims.animate_attack('b', [0, 0, 255], 0.1)

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
    
