# Phenny/Sopel Mumble Module

This is a plugin module for the Python IRC bot [Phenny](http://inamidst.com/phenny/)
and [sopel](http://sopel.chat/)
It provides various commands to access the mumble server (Murmur)

To install this plugin, add the following settings to ~/.phenny/default.py

    mumble_ip     = "127.0.0.1"
    mumle_port    = "6502"
    mumble_slice  = "/path/to/Murmur.ice"
    mumble_secret = "mymumblesecret"
    # Auto alert these channels when someone joins
    mumble_channels = ["#mychannel"]

or for sopel, modify ~/.sopel/default.cfg

    [mumble]
    ip = 127.0.0.1
    port = 6502
    slice = /path/to/Murmur.ice
    secret = mysecret
    channels = #channel1,#channel2,#channel3

Replace the values with values appropriate for your Murmur system.
Murmur.ice should come with your murmur install.
