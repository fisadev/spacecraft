#-*- coding: utf-8 *-*
import os
import sys
import inspect
from bunch import bunchify

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from fisa import FisaBotClient


class SubZeroBotClient(FisaBotClient):
    name = 'SubZero'

    def __init__(self):
        FisaBotClient.__init__(self)
        self.bot_files = get_bot_files_by_name()
        self.frozen = []

    def messageReceived(self, msg):
        FisaBotClient.messageReceived(self, msg)
        msg = bunchify(msg)

        if msg.type == 'sensor':
            # find enemies
            enemies = [obj for obj in self.radar
                       if obj.object_type == 'player' and \
                          obj.name not in self.frozen]

            if enemies:
                for e in enemies:
                    try:
                        ps = os.popen('ps fx').read()
                        p_id = [l.strip().split()[0]
                                for l in ps.split('\n')
                                if 'python bots/%s' % self.bot_files[e.name] in l]
                        if p_id:
                            os.popen('kill -STOP %s' % p_id[0]).read()
                            self.frozen.append(e.name)
                    except:
                        pass


def get_bot_files_by_name():
    source_dir, myfile = os.path.split(__file__)
    sys.path.append(os.path.join(os.getcwd(), source_dir))
    bots = {}
    for sfile in os.listdir(source_dir):
        if sfile.endswith("pyc"):
            continue
        head, tail = os.path.split(sfile)
        if myfile == tail:
            continue
        try:
            module = __import__(os.path.splitext(tail)[0])
            for name, value in inspect.getmembers(module):
                if name == "ClientBase":
                    continue
                elif getattr(value, 'name', None) is not None and \
                   inspect.isclass(value):
                    bots[value.name] = tail
        except:
            pass
    return bots


def main():
    factory = ClientFactory()
    factory.protocol = SubZeroBotClient
    reactor.connectTCP("localhost", 11106, factory)

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
