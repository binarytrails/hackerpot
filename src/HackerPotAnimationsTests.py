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

    pot = {
        'start_led': 0,
        'end_led': 14,
        'rgb': [0, 255, 0]
    }
    
    one = {
        'start_led': 14,
        'end_led': 30,
        'rgb': pot.get('rgb')
    }
    two = {
        'start_led': 30,
        'end_led': 43,
        'rgb': pot.get('rgb')
    }
    three = {
        'start_led': 43,
        'end_led': 60,
        'rgb': pot.get('rgb')
    }

    def __init__(self, serial, max_leds):
        self.SERIAL = serial
        self.MAX_LEDS = max_leds 

    def recolorize(self, delay):
        self.colorize(self.pot['rgb'], delay)
    
    def colorize(self, rgb, delay):
        for led in range(self.MAX_LEDS):
            self.SERIAL.write(bytearray([led] + rgb))
            time.sleep(delay)
    
    def colorize_base(self, start_led, end_led, rgb, delay):
        for led in range(start_led, end_led):
            self.SERIAL.write(bytearray([led] + rgb))
            time.sleep(delay)

    def animate_attack(self, key, rgb, new_rgb, delay):

        stem = None

        if (key == 'one'): stem = self.one
        elif (key == 'two'): stem = self.two
        elif (key == 'three'): stem = self.three

        stem_rgb = stem['rgb']
        start = stem['start_led']
        end = stem['end_led']

        for led in reversed(range(start, end)):
            # new color
            splixel = [led] + rgb
            ser.write(bytearray(splixel))
            time.sleep(delay)

            # make new color influenced by attack
            new_color = [0, 0, 0]

            for i in range(3):
                # influenced by 1/10 of the applied one
                new_color[i] = abs(stem_rgb[i] + (new_rgb[i] / 10))

                if (new_color[i] > 255): new_color[i] = 255

            stem['rgb'] = new_color

            # apply new color
            splixel = [led] + new_color
            self.SERIAL.write(bytearray(splixel))
            time.sleep(delay)

delay = 0.01

anims = HackerPotAnimations(ser, 60)

#anims.colorize([255, 0, 0], delay)
anims.recolorize(delay)

# everything
while 1:

    # connection (evolves into blue)
    anims.animate_attack('one', [0, 0, 255], [0, -255, 255], delay)
    anims.colorize_base(0, 6, anims.one['rgb'], delay)
    
    # intrustion (evolves into red)
    anims.animate_attack('two', [255, 0, 0], [255, -255, 0], delay)
    anims.colorize_base(9, 14, anims.two['rgb'], delay)

    # dos (evolves into purple)
    anims.animate_attack('three', [80, 0, 80], [80, -255, 80], delay)
    anims.colorize_base(6, 9, anims.three['rgb'], delay)
