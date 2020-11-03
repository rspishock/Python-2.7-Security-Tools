#! /usr/bin/python
"""A simple script to verify TCP connectivity by sending a GET request to www.google.com"""

import socket

target_host = 'www.google.com'
target_port = 80

# create a socket object, IPv4 TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
print 'Connecting to %s over port %d' % (target_host, target_port)
client.connect((target_host, target_port))

# send some data
print 'Sending GET request'
client.send(bytes("GET / HTTP/1.1\r\nHost: %s\r\n\r\n") % target_host)

# receive some data
print 'Receiving data'
response = client.recv(4096)

print response
