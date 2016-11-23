import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class HackerPot:

    hackers = dict()

    def __init__(self):
        pass

    def connection(self, peer):
        print('Connection Detected from %s' % peer.host)

        if not peer.host in self.hackers:
            self.hackers[peer.host] = {'connections': 1, 'intrusions': 0}
        else:
            self.hackers[peer.host]['connections'] += 1

    def intrusion(self, peer):
        print('Intrusion Detected from %s' % peer.host)

        if not peer.host in self.hackers:
            self.hackers[peer.host] = {'connections': 0, 'intrusions': 1}
        else:
            self.hackers[peer.host]['intrusions'] += 1

