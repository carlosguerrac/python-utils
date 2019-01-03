import datetime
import telnetlib
import re
import logging
import time
import socket
import sys

def sendTelnetCommand(comando, prompt):

    try:
        logging.info(comando)
        tn.write(comando)
        respuesta = tn.read_until(prompt, 5)
        logging.info(respuesta)
        return respuesta
    except:
        #pass
        return None

def telnetGetCommand(host, user, passwd, comando ):

    prompt = "#"

    user_prompt   = "Username:"
    passwd_prompt = "Password:"

    has_config_changed = False
    port_whitelist = [1,25,26,27,28]

    try:
        print "Accediendo a %s" % host
        tn = telnetlib.Telnet(host)
        #tn.set_debuglevel(1)
        tn.read_until(user_prompt)
        tn.write(user + "\n")
        tn.read_until(passwd_prompt)
        tn.write(passwd + "\n")
        tn.read_until(prompt )

        logging.info(comando)
        tn.write("terminal length 0\n")
        tn.read_until(prompt )
        tn.write(comando+"\n")
        value = tn.read_until(prompt )
        print value
        logging.info(value)

        tn.close()


    except:
        response = 'Failed learned'
    finally:
        print "."


cur_time = time.strftime("%Y%m%dT%H%M%S", time.localtime())

host = sys.argv[1]

#host = '10.17.253.2'

path    = "/home/noc/LOG-sesiones/"
logfile = 'LOG-'+host+'_'+cur_time+'.log'
user   = "comunicaciones"
passwd = "*******"

logging.basicConfig(filename=path+logfile,filemode='a',level=logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %I:%M:%S %p')

try:
    tn = telnetlib.Telnet(host)
except socket.timeout:
#        logging.info("%s socket timeout", host)
        pass
except:
    raise

try:
    telnetGetCommand(host, user, passwd, "show dlsw peer")
    telnetGetCommand(host, user, passwd, "show dlsw cir")
except:
    print "error"
