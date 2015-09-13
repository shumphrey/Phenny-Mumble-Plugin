#!/usr/bin/env python
"""
mumble.py - Phenny Mumble Module
Copyright 2012, Steven Humphrey
Licensed under the Eiffel Forum License 2.

To get this to work, please add 4 keys to the config:
mumble_ip, mumble_port, mumble_slice, mumble_secret.
mumble_slice should be the path to the Murmur.ice file.

http://mumble.sourceforge.net/Ice
"""

import Ice
import threading, time

def setup(self):
    """Sets up ICE"""
    slicefile = self.config.mumble_slice
    icesecret = self.config.mumble_secret

    Ice.loadSlice('', ['-I' + Ice.getSliceDir(), slicefile ] )
    prop = Ice.createProperties([])
    prop.setProperty('Ice.Default.EncodingVersion', '1.0')
    prop.setProperty("Ice.ImplicitContext", "Shared")
    prop.setProperty("Ice.MessageSizeMax",  "65535")

    idd = Ice.InitializationData()
    idd.properties = prop
    global ice
    ice = Ice.initialize(idd)
    ice.getImplicitContext().put("secret", icesecret.encode("utf-8"))
    global Murmur
    import Murmur
    ## Set up threaded checker
    print "set up and now starting timer thread"
    t = threading.Timer(20.0, mumble_auto_loop, [self])
    t.start()


def mumble_auto_loop(phenny):
    server = get_server(phenny)
    users = server.getUsers()
    usernames = []
    recip = phenny.config.mumble_channels
    for key in users:
        name = users[key].name
        usernames.append(name)
    if len(usernames) == 1:
        for r in recip:
            phenny.msg(r, ", ".join(usernames) + " is currently on mumble")
    elif len(usernames) > 0:
        for r in recip:
            phenny.msg(r, ", ".join(usernames) + " are currently on mumble")

    while(True):
        time.sleep(10)
        server = get_server(phenny)
        users = server.getUsers()
        currentusers = []

        joined_users = []
        parted_users = []
        for uk in users:
            currentusers.append(users[uk].name)
        for name in currentusers:
            try:
                usernames.index(name)
            except:
                joined_users.append(name)
                usernames.append(name)
        for name in usernames:
            try:
                currentusers.index(name)
            except:
                parted_users.append(name)
                usernames.remove(name)
        if len(parted_users) > 1 and len(usernames) == 0:
            for r in recip:
                phenny.msg(r,  + "There are no more users connected to mumble")
        if joined_users:
            message = ", ".join(joined_users)
            if len(joined_users) > 1:
                message = message + " have joined mumble"
            else:
                message = message + " has joined mumble"
            for r in recip:
                phenny.msg(r, message)

def get_server(phenny):
    """Returns the mumble server"""
    mumble_ip     = phenny.config.mumble_ip
    mumble_port   = phenny.config.mumble_port or "6502"

    if not mumble_ip:
        phenny.say("mumble is not configured")
        return
        
    connstring = "Meta:tcp -h %s -p %s" % (mumble_ip, mumble_port)

    global ice
    proxy = ice.stringToProxy( connstring.encode("utf-8") )

    global Murmur
    meta = Murmur.MetaPrx.checkedCast(proxy)
    server = meta.getServer(1)
    return server


def mumble_send(phenny, input):
    """Sends a message to mumble server"""
    server = get_server(phenny)
    message = input.group(2)
    if message:
        server.sendMessageChannel(0, False, message)
        phenny.say("Message sent to first channel tree")
    else:
        phenny.say("usage: .mumblesend some text")

mumble_send.commands = ['mumblesend']
mumble_send.priority = 'medium'


def mumble_users(phenny, input): 
    """Shows the users connected to mumble."""
    server = get_server(phenny)

    users = server.getUsers()
    if len(users) == 0:
        phenny.say("No users connected to mumble")
        return
    names = []
    for key in users:
        name = users[key].name
        names.append(name)
    phenny.say("Mumble users: " + ", ".join(names))

mumble_users.commands = ['mumble']
mumble_users.priority = 'medium'


if __name__ == '__main__': 
   print __doc__.strip()
