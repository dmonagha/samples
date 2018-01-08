#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse

parser = argparse.ArgumentParser(description='Used to match IP addresses to their subnet ¯\_(ツ)_/¯')
parser.add_argument('-i', '--input', nargs='?',
    help="Specifies the input file")
parser.add_argument("-o", "--output", 
    type=argparse.FileType('w'), nargs='?', const=sys.stdout,
    help="Specifies the output file")
args = parser.parse_args()

if(args.output is not None):
	sys.stdout = args.output
inputfile = args.input

def main():  
		
	with open(inputfile, 'r') if (args.input is not None) \
	else open(raw_input("Enter the path of the file you want to check: "),'r') as fp: 
	
		print("{:20} {:^20} {:>20}".format("Source IP","Destination Subnet","In Subnet?"))
		
		for line in fp:
			ip1, ip2 = map(str, line.split(","))
  			ip2 = ip2.rstrip("\n\r")
   		
   			cidr = int((ip2.rsplit('/', 1))[1]) #split off the CIDR notation
   			ip2 = ip2.split('/', 1)[0] #split off dest IP
   		
			binip1 = bin(int(ip1,0))[2:].zfill(32) #conv hex src IP to bin and pad with zero
   			binip2 = ''.join([bin(int(x)+256)[3:] for x in ip2.split('.')]) #conv dest IP dotdec to bin
   			bincidr = bin(0xffffffff >> (32-cidr) << (32-cidr))[2:] #conv CIDR notation to bin
   		
   			dotcidr = dotConvert(bincidr)
   			dotip1 = dotConvert(binip1)

			netid1 = netCalc(bincidr,binip1)
			netid2 = netCalc(bincidr,binip2)

			if (netid1 == netid2) and (args.output is not None):
				print("{:<20} {:^20} {:>17}".format(dotip1, dotcidr, " Yes "))
			elif (netid1) == (netid2):
				print("{:<20} {:^20} {:>31}".format(dotip1, dotcidr, "\x1b[0;32;40m Yes \x1b[0m"))
			elif (netid1 != netid2) and (args.output is not None):
				print("{:<20} {:^20} {:>16}".format(dotip1, dotcidr, "No"))
			else:
				print("\x1b[0;31;40m{:<20} {:^20} {:>15} \x1b[0m".format(dotip1, dotcidr, "No"))

def dotConvert(binaddr): #used to convert binary addresss to dotdec
	x = 8
	binlist = [binaddr[i: i + x] for i in range(0, len(binaddr), x)] 
   	dotdec = '.'.join([str(int(num, 2)) for num in binlist]) 
   	return dotdec;

def netCalc(cidr, addr): #used to perform bitwise AND to calc netmask
	cidr = int(cidr, 2)
	addr =  int(addr, 2)
	netid = cidr & addr
	return netid;

if __name__ == '__main__':  
   main()
