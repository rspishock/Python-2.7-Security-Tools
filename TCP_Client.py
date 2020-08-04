#! /usr/bin/python
"""A simple TCP client"""

import optparse
import socket

parser = optparse.OptionParser()

parser.add_option('-t', '--target', dest='target', help="Enter target to connect to")
parser.add_option('-p', '--p', dest='port', help='Enter TCP port to connect to.')

(options, arguments) = parser.parse_args()

target = options.target
port = options.port

target_host = target
target_port = int(port)

# create a socket object, IPv4 TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
print 'Connecting to %s over port %d' % (target_host, target_port)
client.connect((target_host, target_port))

# send some data
print 'Sending GET request'
client.send(bytes("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"))

# receive some data
print 'Receiving data'
response = client.recv(4096)

print response
