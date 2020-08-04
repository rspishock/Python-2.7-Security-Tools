#! /usr/bin/python
"""A simple TCP server."""

import threading
import optparse
import socket

parser = optparse.OptionParser()

parser.add_option('-p', '--p', dest='port', help='Enter TCP port to connect to.')

(options, arguments) = parser.parse_args()

port = options.port
target_port = int(port)

bind_ip = '0.0.0.0'
bind_port = target_port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print '[-] Listening on %s:%d' % (bind_ip, bind_port)


# This is the client-handling thread
def handle_client(client_socket):
    # Print out what the client sends
    request = client_socket.recv(1024)

    print '[*] Received: %s' % request

    # Send back a packet
    client_socket.send('ACK!')

    client_socket.close()


while True:
    client, addr = server.accept()

    print '[*] Accepted connection from: %s:%d' % (addr[0], addr[1])

    # Spin up client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

server.close((bind_ip, bind_port))  # Releases connection/port
