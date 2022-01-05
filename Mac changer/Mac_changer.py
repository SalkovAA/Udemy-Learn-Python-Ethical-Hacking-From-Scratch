#!/usr/bin/env python
import subprocess
import argparse

parser = argparse.ArgumentParser(description = "Changing MAC address")
parser.add_argument( '--interface', dest='interface', type= str,  help = "Input name interface fo changing MAC address", required = True)
parser.add_argument( '--new_mac', dest='new_mac', type= str,  help = "Input new MAC", required = True)
args = parser.parse_args()

print("[+] Changing MAC address for {} to {}".format(args.interface, args.new_mac))

subprocess.call(["ifconfig", args.interface, "down"])
subprocess.call(["ifconfig", args.interface, "hw", "ether", args.new_mac])
subprocess.call(["ifconfig", args.interface, "up"])