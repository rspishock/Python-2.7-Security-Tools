#! /usr/bin/python
"""A simple TCP Proxy"""

import threading
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
