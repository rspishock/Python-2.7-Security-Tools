#! /usr/bin/python
"""A simple TCP client"""

import socket


target_host = '127.0.0.1'
target_port = 9999

# create a socket object, IPv4 TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
print 'Connecting to %s over port %d' % (target_host, target_port)
client.connect((target_host, target_port))

# send some data
print 'Sending GET request'
client.send('ABCD')

# receive some data
print 'Receiving data'
response = client.recv(4096)

print response
