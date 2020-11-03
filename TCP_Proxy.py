#! /usr/bin/python
"""A simple TCP Proxy"""

import threading
import hexdump
import socket
import sys


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" %(local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print the local connection information
        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to response buffer
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to local client, send it
        if len(remote_buffer):
            print('[<==] Sending %d bytes to localhost.' % len(remote_buffer))
            client_socket.send(remote_buffer)

    # no loop and read from local
    while True:

        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print('[==>] Received %d bytes from localhost.' % len(local_buffer))
            hexdump(local_buffer)

            # send to request handler
            local_buffer = request_handler(local_buffer)

            # send data to remote host
            remote_socket.send(local_buffer)
            print('[==>] Sent to remote.')


def main():
    # no fancy command line parsing
    if len(sys.argv[1:]) != 5:
        print "Usage: TCP_Proxy.py [localhost] [localport] [remotehost] [remoteport] [preceived_first]"
        print "Example: TCP_Prpxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    # local listening parameters
    local_host = sys.argv[1]
    local_port = sys.argv[2]

    # remote target parameters
    remote_host = sys.argv[3]
    remote_port = sys.argv[4]

    # instructs proxy to connect and receive data before sending to the remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # spin up listening socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()