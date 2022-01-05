#!/usr/bin/env python
import subprocess
import argparse
import re


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
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.run(['ifconfig', interface], capture_output=True, text = True).stdout
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result[0]
    else:
        print('[-] Could not read MAC adress')

args = get_arguments()

initial_mac_addres = get_current_mac(args.interface)
print('Initial MAC addres = {}'.format(initial_mac_addres))

change_mac(args.interface, args.new_mac)

new_mac_address = get_current_mac(args.interface)
print('New MAC addres = {}'.format(new_mac_address))

if new_mac_address == args.new_mac:
    print('[+] MAC address was successfully change to {}'.format(new_mac_address))
else:
    print('[-] MAC address did not get changed')
