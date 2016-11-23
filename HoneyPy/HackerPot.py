#from twisted.python import log

class HackerPot:
    def __init__(self):
        pass

    def connection(self, peer):
        print('Connection Detected from %s' % peer.host)

    def intrusion(self, peer):
        print('Intrusion Detected from %s' % peer.host)

