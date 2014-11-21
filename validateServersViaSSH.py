#!/usr/bin/python
#
# Adapted from sample code from Jesse Noller http://jessenoller.com/blog/2009/02/05/ssh-programming-with-paramiko-completely-different
#

import paramiko
import cmd
import getpass
import sys

class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    username = ''
    password = ''
    hosts = []

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host 
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('*** Connecting to ' + str(host))
            client.connect(host, username=self.username, password=self.password)
            self.connections.append(client)

    def do_run(self, command):
        """run 
        Execute this command on all hosts in the list"""
        if len(self.connections) == 0:
            print "  Did you forget to connect?"
            return
        
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command, get_pty=True, timeout=30)
                stdin.close()
                print '  ==============================================================================================='
                for line in stdout.read().splitlines():
                    print('  [%s@%s]%s' % (self.username, host, line))
                print '  ==============================================================================================='

        else:
            print "  usage: run "

    def do_close(self, args):
        """close
        Close all connections"""
        print('  closing all connections')
        for conn in self.connections:
            conn.close()

    def do_quit(self, args):
        """quit
        Quit the tool"""
        self.do_close(args)
        print('Goodbye!')
        sys.exit(0)

if __name__ == '__main__':
    run = RunCommand()
    run.username = raw_input('Enter your username: ')
    run.password = getpass.getpass('Enter your password: ')
    run.hosts = sys.argv[1:]
    print('Using hosts: ' + str(run.hosts))
    run.cmdloop()
