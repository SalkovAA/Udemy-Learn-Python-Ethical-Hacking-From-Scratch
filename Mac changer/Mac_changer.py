#!/usr/bin/env python
import subprocess
import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description = "Changing MAC address")
    parser.add_argument( '--interface', dest='interface', type= str,  help = "Input name interface fo changing MAC address", required = True)
    parser.add_argument( '--new_mac', dest='new_mac', type= str,  help = "Input new MAC", required = True)
    return parser.parse_args()
    #args = parser.parse_args()
    #if not args.interface:
    #    parser.error("[-] Please specify an interface, use --help for more info")
    #elif not args.new_mac:
    #    parser.error("[-] Please specify an new mac, use --help for more info")
    #return args

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for {} to {}".format(interface, new_mac))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


args = get_arguments()
change_mac(args.interface, args.new_mac)