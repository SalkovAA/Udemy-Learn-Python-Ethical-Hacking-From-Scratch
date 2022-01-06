#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description = "Network scanner")
    parser.add_argument( '--target', dest= 'target', type= str,  help= "Input target IP / IP range", required = True)
    return parser.parse_args()

def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)
    clients_list = []
    for element in answered_list:
        clients_list.append({"ip" : element[1].psrc, "mac" : element[1].hwsrc})
    return clients_list

def print_result(result_list):
    print("IP\t\t\tMac Address\n-----------------------------------------")
    for client in result_list:
        print('{}\t\t{}'.format(client['ip'], client['mac']))
    #scapy.arping(ip)

args = get_arguments()
scan_result = scan(args.target)
print_result(scan_result)