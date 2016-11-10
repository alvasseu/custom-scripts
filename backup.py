#!/usr/local/bin/python2.7
from __future__ import with_statement
#Author =  Julien COPPI
import socket
import inspect
from Exscript.protocols.drivers.driver import Driver
from Exscript.protocols import SSH2
from Exscript.protocols.Exception import LoginFailure, InvalidCommandException
from Exscript import Host,Account
import glob
import os
import os.path
import sys
import shutil
from datetime import datetime, timedelta
import time
import paramiko
from scp import SCPClient
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders



###Variables
device_fail = []
connection_error = []
bad_login = []
IOS_list_fail = []
NXOS_list_fail = []
ARISTA_list_fail = []
METAMAKO_list_fail = []
BLADE_list_fail = []
ASA_list_fail = []
FORTINET_list_fail = []
JUNIPER_list_fail = []
A10_list_fail = []
F5_list_fail = []
NETSCALER_list_fail = []
CHECKPOINT_list_fail = []
BLUECOAT_list_fail = []
number_of_devices_saved = 0
number_of_devices_not_saved = 0
IOS_success = 0.0
IOS_fail = 0.0
NXOS_success = 0.0
NXOS_fail = 0.0
ARISTA_success = 0.0
ARISTA_fail = 0.0
METAMAKO_success = 0.0
METAMAKO_fail = 0.0
BLADE_success = 0.0
BLADE_fail = 0.0
ASA_success = 0.0
ASA_fail = 0.0
FORTINET_success = 0.0
FORTINET_fail = 0.0
JUNIPER_success = 0.0
JUNIPER_fail = 0.0
A10_success = 0.0
A10_fail = 0.0
F5_success = 0.0
F5_fail = 0.0
NETSCALER_success = 0.0
NETSCALER_fail = 0.0
CHECKPOINT_success = 0.0
CHECKPOINT_fail = 0.0
BLUECOAT_success = 0.0
BLUECOAT_fail = 0.0


print '##################################################################'
print '##################### CONFIG BACKUP v1############################'
print '##################################################################'



def default_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def asa_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def ne_checkpoint_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def sg_checkpoint_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def fortinet_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def juniper_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def a10_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def f5_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def blade_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def citrix_auth():
    #password = raw_input('What is your password?')
    password = '''xxxxx'''
    account = Account('username',password)
    return account

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


##########################Netscaler Paramiko test
# def netscaler(netscaler_ip):
#     resp = 0
#     try:
#         ip = netscaler_ip
#         port = 22
#         username = 'nsroot'
#         password = 'xxxxx'
#         cmd = 'show running'
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip, port, username, password)
#         stdin, stdout, stderr = ssh.exec_command(cmd)
#         outlines = stdout.readlines()
#         resp = ''.join(outlines)
#     except:
#         resp = 0
#
#     return resp
########################### Fin test Netscaler


####Go in the good directory
#os.chdir("C:/Users/avasseur/PycharmProjects/untitled/BACKUP/")

####Creation of the directory of the day
date_of_the_day = datetime.today().strftime("%Y%m%d")
date_of_last_day = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
print date_of_the_day

####Check if directory exist
if os.path.exists("/home/netadmin/scripts/test/BACKUP/%s"%date_of_the_day):
    ans1 = raw_input('This directory is already existing, do you want to delete it?')
    if ans1.lower() == 'y':
        shutil.rmtree('/home/netadmin/scripts/test/BACKUP/%s'%date_of_the_day)
    else:
        sys.exit()


####Creation of the directory of the day
os.mkdir('/home/netadmin/scripts/test/BACKUP/%s'%date_of_the_day)

####Go in the good directory of the day
os.chdir("/home/netadmin/scripts/test/BACKUP/%s"%date_of_the_day)
print ("/home/netadmin/scripts/test/BACKUP/%s"%date_of_the_day)

os.mkdir('ASA')
os.mkdir('IOS')
os.mkdir('NXOS')
os.mkdir('METAMAKO')
os.mkdir('ARISTA')
os.mkdir('FORTINET')
os.mkdir('JUNIPER')
os.mkdir('A10')
os.mkdir('NETSCALER')
os.mkdir('F5')
os.mkdir('BLADE')

path = '/home/netadmin/scripts/test/devices/*'
files = glob.glob(path)

for file in files:
    f = open(file, 'r')
    model_text = file.split('/')[-1]
    model = model_text.split('.')[0]
    print '----------'
    print model
    print '----------'
    if model == 'IOS':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/IOS/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg'%device_name)

            try:
                conn = SSH2(driver='generic')
                conn.connect(device_name)
                conn.login(default_auth())
                conn.execute('term len 0')
                try:
                    conn.execute('show run')
                    output = conn.response
                    conn.send('exit\n')
                except:
                    print('1rst sh run fail, try enable password')
                    print "Unexpected error:", sys.exc_info()
                    conn.execute('enable')
                    conn.execute('show run')
                    #conn.execute('show run')
                    output = conn.response
                    conn.send('exit\n')
                conn.close()
                if len(output.split('\n')) > 10:
                        conf_wr = open(device_conf, 'a')
                        conf_wr.write(output)
                        conf_wr.close()
                        number_of_devices_saved = number_of_devices_saved + 1
                        IOS_success += 1
                else:
                        device_fail.append(device_name)
                        connection_error.append(device_name)
                        IOS_list_fail.append(device_name)
                        number_of_devices_not_saved = number_of_devices_not_saved + 1
                        IOS_fail += 1
            except socket.error:
                print('Connection Error')
                conn.close()
                device_fail.append(device_name)
                connection_error.append(device_name)
                IOS_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                IOS_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                IOS_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                IOS_fail += 1
            except:
                print('Save failed attempt 1')
                print "Unexpected error:", sys.exc_info()
                try:
                   print "Second attempt"
                   conn = SSH2(driver='ios', verify_fingerprint=False)
                   #print'p1'
                   conn.connect(device_name)
                   conn.login(default_auth())
                   #print'p2'
                   conn.execute('term len 0')
                   conn.execute('show run')
                   output = conn.response
                   conn.send('exit')
                   conn.close()
                   if len(output.split('\n')) > 10:
                        conf_wr = open(device_conf, 'a')
                        conf_wr.write(output)
                        conf_wr.close()
                        number_of_devices_saved = number_of_devices_saved + 1
                        IOS_success += 1
                   else:
                        print('Output too short')
                        device_fail.append(device_name)
                        IOS_list_fail.append(device_name)
                        number_of_devices_not_saved = number_of_devices_not_saved + 1
                        IOS_fail += 1
                except:
                   print 'All attempt failed'
                   device_fail.append(device_name)
                   IOS_list_fail.append(device_name)
                   number_of_devices_not_saved = number_of_devices_not_saved + 1
                   IOS_fail += 1

    elif model == 'ASA':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/ASA/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)
            account = Account('username',password = '''xxxxx''',password2 = '''xxxxx''')

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(account)
                #conf_wr = open(device_conf, 'a')
                conn.send('enable\r')
                conn.auto_app_authorize(account)
                conn.execute('terminal pager 0')
                #2 time show run to correct bug, otherwise the last execute command is not in the output
                conn.execute('show run')
                output = conn.response
                if len(output.split('\n')) < 10:
                        print'Output empty'
                        conn.execute('show run')
                        output = conn.response
                else:
                        #conn.execute('show run')
                        #output = conn.response
                        pass
                conn.send('exit')
                conn.close()
                if len(output.split('\n')) > 10:
                        conf_wr = open(device_conf, 'a')
                        conf_wr.write(output)
                        conf_wr.close()
                        number_of_devices_saved = number_of_devices_saved + 1
                        ASA_success += 1
                else:
                        print('Output too short')
                        device_fail.append(device_name)
                        ASA_list_fail.append(device_name)
                        number_of_devices_not_saved = number_of_devices_not_saved + 1
                        ASA_fail += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                ASA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ASA_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                ASA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ASA_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()[0]
                device_fail.append(device_name)
                ASA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ASA_fail += 1


    elif model == 'NXOS':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/NXOS/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(default_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('term len 0')
                conn.execute('show run')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                NXOS_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                NXOS_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NXOS_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                NXOS_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NXOS_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                NXOS_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NXOS_fail += 1


    elif model == 'BLADE':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/BLADE/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg'%device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(default_auth())
                conf_wr = open(device_conf, 'a')
                try:
                    conn.execute('term len 0')
                except:
                    conn.execute('terminal-length 0')
                    #continue
                conn.execute('show run')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                BLADE_success += 1
                conn.send('exit')
                conn.close()
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                BLADE_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                BLADE_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                BLADE_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                BLADE_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                BLADE_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                BLADE_fail += 1


    elif model == 'METAMAKO':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/METAMAKO/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2(driver='generic')
                conn.connect(device_name)
                conn.login(default_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('enable')
                conn.execute('show run')
                output = conn.response
                conf_wr.write(output)
                conn.send('exit')
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                METAMAKO_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                METAMAKO_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                METAMAKO_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                METAMAKO_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                METAMAKO_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                METAMAKO_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                METAMAKO_fail += 1

    elif model == 'ARISTA':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/ARISTA/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(default_auth())
                conf_wr = open(device_conf, 'a')
                ###To avoid error
                time.sleep(1)
                conn.execute('term len 0')
                conn.execute('show run')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                ARISTA_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                ARISTA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ARISTA_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                ARISTA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ARISTA_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                ARISTA_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                ARISTA_fail += 1

    elif model == 'FORTINET':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/FORTINET/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                port = 22
                user = 'username'
                password = 'xxxx'
                ssh = createSSHClient(device_name, port, user, password)
                scp = SCPClient(ssh.get_transport())
                scp.get('sys_config','/home/netadmin/scripts/test/BACKUP/%s/FORTINET/%s'%(date_of_the_day,device_conf))
                number_of_devices_saved = number_of_devices_saved + 1
                FORTINET_success += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                FORTINET_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                FORTINET_fail += 1


    elif model == 'JUNIPER':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/JUNIPER/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(juniper_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('set console page 0')
                conn.execute('get config')
                output = conn.response
                conn.execute('set console page 20')
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                JUNIPER_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                JUNIPER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                JUNIPER_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                JUNIPER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                JUNIPER_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                JUNIPER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                JUNIPER_fail += 1

    elif model == 'A10':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/A10/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s'%device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.login(default_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('term len 0')
                conn.execute('show running')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                A10_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                A10_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                A10_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                A10_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                A10_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                A10_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                A10_fail += 1


    elif model == 'NETSCALER':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/NETSCALER/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s' % device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.set_prompt('>')
                conn.login(citrix_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('show running')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                NETSCALER_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                NETSCALER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NETSCALER_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                NETSCALER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NETSCALER_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                NETSCALER_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                NETSCALER_fail += 1


    ####################NETSCALER TEST PARAMIKO
    #  elif model == 'NETSCALER':
    #     for line in f:
    #         os.chdir("C:/Users/avasseur/PycharmProjects/untitled/BACKUP/%s/NETSCALER/" % date_of_the_day)
    #         device_name = line.replace('\n', '')
    #         print ('  %s'%device_name)
    #         device_conf = ('%s.cfg' % device_name)
    #         conf_wr = open(device_conf, 'a')
    #
    #         netscaler_conf = str(netscaler(device_name))
    #
    #         if netscaler_conf == '0':
    #             print('Save failed')
    #             device_fail.append(device_name)
    #             number_of_devices_not_saved = number_of_devices_not_saved + 1
    #         else:
    #             conf_wr.write(netscaler_conf)
    #             conf_wr.close()
    #             number_of_devices_saved = number_of_devices_saved + 1
    ################TIN TEST NETSCALER


    elif model == 'F5':
        for line in f:
            os.chdir("/home/netadmin/scripts/test/BACKUP/%s/F5/" % date_of_the_day)
            device_name = line.replace('\n', '')
            print ('  %s' % device_name)
            device_conf = ('%s.cfg' % device_name)

            try:
                conn = SSH2()
                conn.connect(device_name)
                conn.set_prompt('#')
                conn.login(f5_auth())
                conf_wr = open(device_conf, 'a')
                conn.execute('cat /config/bigip.conf')
                output = conn.response
                conf_wr.write(output)
                conf_wr.close()
                number_of_devices_saved = number_of_devices_saved + 1
                F5_success += 1
            except socket.error:
                print('Connection Error')
                device_fail.append(device_name)
                connection_error.append(device_name)
                F5_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                F5_fail += 1
            except LoginFailure:
                print ('Login Fail')
                device_fail.append(device_name)
                bad_login.append(device_name)
                F5_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                F5_fail += 1
            except:
                print('Save failed')
                print "Unexpected error:", sys.exc_info()
                device_fail.append(device_name)
                F5_list_fail.append(device_name)
                number_of_devices_not_saved = number_of_devices_not_saved + 1
                F5_fail += 1


print ('\n')
print ('\n')
print '##################################################################'
print '#####################  Script Result  ############################'
print '##################################################################'
print ('\n')
print ('The script had correctly saved : %i devices' %number_of_devices_saved)
print ('The script had failed to save : %i devices' %number_of_devices_not_saved)
print ('\n')
if number_of_devices_not_saved != 0:
    print ('%i Devices not correctly saved:' %number_of_devices_not_saved)
    for object in device_fail:
        print ('  %s'%object)

list_of_device_fail = '\n  '.join(device_fail)


import conf_change

conf_change.configuration_compare()


############## Generate Summary Mail

date_du_jour = time.strftime('%Y-%m-%d')

IOS_percent = '{0:.0%}'.format(IOS_success/(IOS_success+IOS_fail))
NXOS_percent = '{0:.0%}'.format(NXOS_success / (NXOS_success + NXOS_fail))
ARISTA_percent = '{0:.0%}'.format(ARISTA_success / (ARISTA_success + ARISTA_fail))
METAMAKO_percent = '{0:.0%}'.format(METAMAKO_success / (METAMAKO_success + METAMAKO_fail))
BLADE_percent = '{0:.0%}'.format(BLADE_success / (BLADE_success + BLADE_fail))
FORTINET_percent = '{0:.0%}'.format(FORTINET_success / (FORTINET_success + FORTINET_fail))
JUNIPER_percent = '{0:.0%}'.format(JUNIPER_success / (JUNIPER_success + JUNIPER_fail))
ASA_percent = '{0:.0%}'.format(ASA_success / (ASA_success + ASA_fail))
A10_percent = '{0:.0%}'.format(A10_success / (A10_success + A10_fail))
NETSCALER_percent = '{0:.0%}'.format(NETSCALER_success / (NETSCALER_success + NETSCALER_fail))
F5_percent = '{0:.0%}'.format(F5_success / (F5_success + F5_fail))
#CHECKPOINT_percent = '{0:.0%}'.format(CHECKPOINT_success / (CHECKPOINT_success + CHECKPOINT_fail))
#BLUECOAT_percent = '{0:.0%}'.format(BLUECOAT_success / (BLUECOAT_success + BLUECOAT_fail))


body = ("""
Backup Script Report - %s
-----------------------------------------------------

.: This backup script is still in development :.


The script had correctly saved : %i devices

The script had failed to save : %i devices

Cisco IOS : %s
Cisco NXOS : %s
Cisco Blade : %s
Arista : %s
Metamako : %s
ASA/FWSM : %s
Fortinet : %s
Juniper : %s
A10 : %s
Netscaler : %s
F5 : %s


List of devices not saved:
  %s

Backup directory:
/scripts/test/BACKUP/%s/

You can check the configuration change on:
/scripts/test/BACKUP/%s/Configuration_changes_%s.txt

Have a nice day.

""" %(date_du_jour,number_of_devices_saved,number_of_devices_not_saved,IOS_percent,NXOS_percent,BLADE_percent,ARISTA_percent,METAMAKO_percent,ASA_percent,FORTINET_percent,JUNIPER_percent,
A10_percent,NETSCALER_percent,F5_percent,list_of_device_fail,date_of_the_day,date_of_the_day,date_of_the_day))

msg = MIMEMultipart()

fromaddr = "test"
toaddr = ["test1", "test2", "test3"]
#"test4m"


msg["From"] = fromaddr
msg["To"] = ', '.join(toaddr)
msg["Subject"] = ("BACKUP SCRIPT REPORT - %s"%date_du_jour)

msg.attach(MIMEText(body, 'plain'))

if os.path.isfile("/scripts/test/BACKUP/%s/Configuration_changes_%s.txt"%(date_of_the_day,date_of_the_day)):
        filename = ("Configuration_changes_%s.txt"%date_of_the_day)
        attachment = open("/scripts/test/BACKUP/%s/Configuration_changes_%s.txt"%(date_of_the_day,date_of_the_day), "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
else:
        pass


server = smtplib.SMTP('localhost')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()








#Author = BOGOSS
import os
import time
from datetime import datetime, timedelta
import glob
import difflib
import filecmp

def configuration_compare():

    def command_compare_diff_conf(line):
        if 'ntp clock-period' in line:
            return False
        else:
            return True


    def command_blade_diff_conf(line):
        if 'access user administrator-password' in line or 'ekey' in line or 'ntp clock-period' in line:
            return False
        else:
            return True

    def line_counter(line_number,line_removed,line_added,line_changed):
        line_number = line_number + 1
        if line.startswith('?  ') and (line_removed == 1 or line_added == 1):
            line_number = line_number - 1
            line_changed = 1
        elif line.startswith('- '):
            line_removed = 1
        elif line.startswith('+ ') and line_removed == 1:
            line_number = line_number - 1
            line_added = 1
            line_removed = 0
        else:
            line_added = 0
            line_removed = 0
            line_changed = 0
        return line_number,line_removed,line_added,line_changed

    date_of_the_day = time.strftime("%Y%m%d")
    date_of_last_day = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")

    path1 = ("/scripts/test/BACKUP/%s/*/*"%date_of_the_day)
    path2 = ("/scripts/test/BACKUP/%s/*/*"%date_of_last_day)
    files1 = glob.glob(path1)
    files2 = glob.glob(path2)
    summary=[]
    number_of_config_changed = 0

    #print '##################################################'
    #print '########  Script Configuration changes  ##########'
    #print '##################################################'
    #print '\n'
    #print 'Script is processing...'
    for file1 in files1:

        if os.path.isfile(file1.replace('%s' % date_of_the_day, '%s' % date_of_last_day)):
            if (filecmp.cmp(file1,file1.replace('%s' % date_of_the_day, '%s' % date_of_last_day),shallow=False)) == True:
                #print 'ok'
                pass
            else:
                #print 'nok'

                device_txt = file1.split('/')[-1]
                device_name = device_txt.split('.')[0]
                #print device_name
                diff = difflib.ndiff(open(file1.replace('%s' % date_of_the_day, '%s' % date_of_last_day)).readlines(),open(file1).readlines())
                #print ''.join(diff)

                ###use conf_start to avoid the compare of the beginning conf file
                conf_start = 0
                if 'IOS' in file1:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
                    for line in diff:
                        line_number, line_removed, line_added, line_changed = line_counter(line_number, line_removed,line_added, line_changed)

                        if 'version' in line:
                            conf_start = 1
                        if conf_start==1 and (line.startswith('-') or line.startswith('+')) and command_compare_diff_conf(line)==True:
                            #print line.replace('\n','')

                            conf_changed.append('Line %i: %s'%(line_number,line.replace('\n','')))

                    if not conf_changed:
                        pass
                    else:
                        summary.append('\n')
                        summary.append('\n')
                        summary.append(device_name)
                        summary.append('\n')
                        summary.append('------------------------------------------------')
                        summary.append('\n')
                        for object in conf_changed:
                            summary.append(''.join(object))
                        summary.append('\n')
                        number_of_config_changed = number_of_config_changed + 1
                    #line_number = line_number + 1

                elif 'NXOS' in file1:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
                    for line in diff:

                        line_number, line_removed, line_added, line_changed = line_counter(line_number,line_removed,line_added,line_changed)

                        if 'version' in line:
                            conf_start = 1

                        if conf_start == 1 and (line.startswith('-') or line.startswith('+')):
                            #print line.replace('\n','')
                            conf_changed.append('Line %i: %s'%(line_number, line.replace('\n', '')))


                    if not conf_changed:
                        pass
                    else:
                        summary.append('\n')
                        summary.append('\n')
                        summary.append(device_name)
                        summary.append('\n')
                        summary.append('------------------------------------------------')
                        summary.append('\n')
                        for object in conf_changed:
                            summary.append(''.join(object))
                        summary.append('\n')
                        number_of_config_changed = number_of_config_changed + 1

                elif 'BLADE' in file1:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
                    for line in diff:
                        line_number, line_removed, line_added, line_changed = line_counter(line_number, line_removed,line_added, line_changed)

                        if 'configuration' in line:
                            conf_start = 1
                        if conf_start==1 and (line.startswith('-') or line.startswith('+')) and command_blade_diff_conf(line)==True:
                            #print line.replace('\n','')

                            conf_changed.append('Line %i: %s'%(line_number,line.replace('\n','')))

                    if not conf_changed:
                        pass
                    else:
                        summary.append('\n')
                        summary.append('\n')
                        summary.append(device_name)
                        summary.append('\n')
                        summary.append('------------------------------------------------')
                        summary.append('\n')
                        for object in conf_changed:
                            summary.append(''.join(object))
                        summary.append('\n')
                        number_of_config_changed = number_of_config_changed + 1
                    #line_number = line_number + 1



                elif 'METAMAKO' in file1:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
                    for line in diff:
                        line_number, line_removed, line_added, line_changed = line_counter(line_number, line_removed,line_added, line_changed)

                        if line.startswith('hostname'):
                            conf_start = 1
                        if conf_start==1 and (line.startswith('-') or line.startswith('+')) and command_compare_diff_conf(line)==True:
                            #print line.replace('\n','')

                            conf_changed.append('Line %i: %s'%(line_number,line.replace('\n','')))

                    if not conf_changed:
                        pass
                    else:
                        summary.append('\n')
                        summary.append('\n')
                        summary.append(device_name)
                        summary.append('\n')
                        summary.append('------------------------------------------------')
                        summary.append('\n')
                        for object in conf_changed:
                            summary.append(''.join(object))
                        summary.append('\n')
                        number_of_config_changed = number_of_config_changed + 1
                    #line_number = line_number + 1



                elif 'FORTINET' in file1:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
#                    for line in diff:
#                        line_number, line_removed, line_added, line_changed = line_counter(line_number, line_removed,
#                                                                                           line_added, line_changed)
#                        ###This permit to detect is the conf hash changed
#                        if '- #conf_file_ver' in line or '+ #conf_file_ver' in line:
#                            conf_start = 1
#                        elif '-----BEGIN' in line:
#                            conf_start = 0
#                        elif'-----END' in line:
#                            conf_start = 1
#
#                        if conf_start == 1 and (
#                            line.startswith('-') or line.startswith('+')) and command_compare_diff_conf(line) == True:
#                            # print line.replace('\n','')
#
#                            conf_changed.append('Line %i: %s' % (line_number, line.replace('\n', '')))
#
#                    if not conf_changed:
#                        pass
#                    else:
#                        summary.append('\n')
#                       summary.append('\n')
#                        summary.append(device_name)
#                       summary.append('\n')
#                        summary.append('------------------------------------------------')
#                       summary.append('\n')
#                        for object in conf_changed:
#                            summary.append(''.join(object))
#                        summary.append('\n')
#                        number_of_config_changed = number_of_config_changed + 1


                else:
                    conf_changed = []
                    line_number = 0
                    line_removed = 0
                    line_added = 0
                    line_changed = 0
                    for line in diff:

                        line_number, line_removed, line_added, line_changed = line_counter(line_number, line_removed,line_added, line_changed)

                        if line.startswith('-') or line.startswith('+'):
                            #print line.replace('\n', '')
                            conf_changed.append('Line %i: %s'%(line_number,line.replace('\n','')))

                    if not conf_changed:
                        pass
                    else:
                        summary.append('\n')
                        summary.append('\n')
                        summary.append(device_name)
                        summary.append('\n')
                        summary.append('------------------------------------------------')
                        summary.append('\n')
                        for object in conf_changed:
                            summary.append(''.join(object))
                        summary.append('\n')
                        number_of_config_changed = number_of_config_changed + 1


    if number_of_config_changed == 0:
        print 'No config changed today.'
        pass
    else:
        print 'Configs changed'
       os.chdir("/scripts/test/BACKUP/%s"%date_of_the_day)
        change_wr = open('Configuration_changes_%s.txt'%date_of_the_day, 'a')
        #print '\n'
        #print '##################################################'
        #print '########    Configuration changes   ##############'
        #print '##################################################'
        #print('%i configuration changed since yesterday.'%number_of_config_changed)
        change_wr.write('##################################################\n')
        change_wr.write('########    Configuration changes   ##############\n')
        change_wr.write('##################################################\n')
        change_wr.write('\n')
        change_wr.write('%i configuration changed since yesterday.\n'%number_of_config_changed)
        change_wr.write('\n')
        for line in summary:
            #print ''.join(line)
            change_wr.write(''.join(line))
            change_wr.write('\n')


#configuration_compare()
