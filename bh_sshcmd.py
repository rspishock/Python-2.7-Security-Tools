#! /usr/bin/python
"Creates a connection to an SSH server and runs a single command."

import subprocess
import threading
import paramiko


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load host_keys('/home/ryan/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return


ssh_command('192.168.100.131', 'ryan', 'password', 'id')
