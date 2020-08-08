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
    print 'Usage: nc.py -t --target <target_host> -p --port <port>'
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


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu', ['help', 'listen', 'execute', 'target', 'port', 'command'
                                                                , 'upload'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = True
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert  False, "Unhandled Option"


    # listen or just send data
    if not listen and len(target) and port > 0:
        # read in the buffer from the command line
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)


    # listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on command line options above
    if listen:
        server_loop()


main()