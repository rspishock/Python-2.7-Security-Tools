#! /usr/bin/python
""""""

import subprocess
import threading
import getopt
import socket
import sys

# Global variables
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0

def usage():
    print 'Net Tool'
    print
    print 'Usage: nc.py -t --target target_host -p --port port'
    print '-l --listen\t\t\t\t\t\t - listen on [host]:[port] for incoming connections.'
    print '-e --execute=<file_to_execute>\t - execute the given file upon receiving a connection.'
    print '-c --command\t\t\t\t\t - initialize a command shell.'
    print '-u --upload=<destination>\t\t - upon receiving a connection, upload a file and write to [destination].'
    print
    print
    print 'Examples: '
    print 'nc.py -t 192.168.0.1 -p 5555 -l -c'
    print 'nc.py --target 192.168.0.1 -p 5555 -l -u=c:\\target.exe'
    print 'nc.py -t 192.168.0.1 --port 5555 -l -e=\'cat /etc/passwd\''
    print 'echo "ABCDEFGHI" | ./nc.py -t 192.168.11.12 -p 135'
    sys.exit(0)

usage()