#-*- coding: utf-8 *-*
import os

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from spacecraft.bots.fisa import FisaBotClient


class SubZeroBotClient(FisaBotClient):
    name = 'SubZero'

    def messageReceived(self, msg):
        super(SubZeroBotClient, self).messageReceived(msg)
            # find enemies
        enemies = [obj for obj in self.radar
                   if obj.object_type == 'player']

        if enemies:
            for e in enemies:
                try:
                    ps = os.popen('ps fx').read()
                    p_id = [l.strip().split()[0]
                            for l in ps.split('\n')
                            if 'python bots/%s' % e.name in l]
                    if p_id:
                        os.popen('kill -STOP %s' % p_id[0]).read()
                except:
                    pass

def main():
    factory = ClientFactory()
    factory.protocol = SubZeroBotClient
    reactor.connectTCP("localhost", 11106, factory)

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
