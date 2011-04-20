#!/usr/bin/env python

#Python libraries (preinstalled)
import datetime
import hashlib
import os
import random
import sys
import time
import urllib

#Twisted libraries (dependency- you must install zope.interface as well)
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor

class MyBot(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname

    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        print "*** Joined " + channel
        self.myDict = {}

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        if '++' in msg:
            if msg.endswith('--'):
                if msg.split('++')[0] == user:
                    self.msg(channel,"You can't plus yourself")
                    return
                try:
                    self.myDict[msg.split('++')[0]] += 1
                    print "+1 for %s" % user
                    return
                except:
                    self.myDict[msg.split('++')[0]] = 1
                    print "The first +1 for %s" % user
                    return
        if '--' in msg:
            if msg.endswith('--'):
                try:
                    self.myDict[msg.split('--')[0]] = self.myDict[msg.split('--')[0]] - 1
                    print "-1 for "+user
                    return
                except:
                    self.myDict[msg.split('--')[0]] = -1
                    print "The first -1 for %s" % user
                    return
        if msg.split()[0] == 'print':
            try:
                msgToDisplay = msg.split()[1] + ": " + str(self.myDict[msg.split()[1]])
                self.msg(channel,msgToDisplay)
                print "I answered to %s: %s" % (user,msgToDisplay)
                return
            except:
                self.msg(channel,"Non-existing member: %s" % msg.split()[1])
                print "Non-existing member: %s" % msg.split()[1]


class MyBotFactory(protocol.ClientFactory):
    protocol = MyBot

    def __init__(self, channel, nickname='scoreBot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

def main():
    network = 'irc.freenode.net'
    reactor.connectTCP(network, 6667, MyBotFactory('#python-forum'))
    reactor.run()

if __name__ == "__main__":
    main()
