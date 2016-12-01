#!/usr/bin/env python3

import time
import serial
import Queue

class HackerPot:

    LEDS = 60

    ATTACK_ANIM_DELAY = 0.1

    SERIAL = serial.Serial( 
        port='/dev/ttyAMA0',
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    hackers = dict()
    
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

    def __init__(self):
        #self.colorize([255, 0, 0], 0.01)
        self.recolorize(0.01)

    # hackers interactions

    def connection(self, peer):
        print('Connection Detected from %s' % peer.host)

        if not peer.host in self.hackers:
            self.hackers[peer.host] = {'connections': 1, 'intrusions': 0}
        else:
            self.hackers[peer.host]['connections'] += 1

        # connection (evolves into blue)
        self.animate_attack('one',
                            [0, 0, 255],
                            [0, -255, 255],
                            self.ATTACK_ANIM_DELAY,
                            reduce_by = 20)

    def intrusion(self, peer):
        print('Intrusion Detected from %s' % peer.host)

        if not peer.host in self.hackers:
            self.hackers[peer.host] = {'connections': 0, 'intrusions': 1}
        else:
            self.hackers[peer.host]['intrusions'] += 1
    
        # intrustion (evolves into red)
        self.animate_attack('three',
                            [255, 0, 0],
                            [255, -255, 0],
                            self.ATTACK_ANIM_DELAY,
                            reduce_by = 5)

    # animations

    def recolorize(self, delay):
        self.colorize(self.pot['rgb'], delay)
    
    def colorize(self, rgb, delay):
        for led in range(self.LEDS):
            self.SERIAL.write(bytearray([led] + rgb))
            time.sleep(delay)

    def animate_attack(self, key, rgb, new_rgb, delay, reduce_by):
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
            self.SERIAL.write(bytearray(splixel))
            time.sleep(delay)

            # make new color influenced by attack
            new_color = [0, 0, 0]

            for i in range(3):
                # influenced by 1/10 of the applied one
                new_color[i] = abs(stem_rgb[i] + (new_rgb[i] / reduce_by))

                if (new_color[i] > 255): new_color[i] = 255

            stem['rgb'] = new_color

            # apply new color
            splixel = [led] + new_color
            self.SERIAL.write(bytearray(splixel))
            time.sleep(delay)

