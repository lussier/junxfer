# Author: 	Gregory A. Lussier
# Subject:	VRRP Configuration Generation
#
# Description:
# Takes an existing legacy configuration and turns it into
# the primary router's configuration of an active/passive
# core network between two Juniper SRX routers.
#
# The IP address of the primary router ends in .252 and the
# IP address of the secondary router ends in .253. Default
# gateways remain untouched at .254.

import copy
 
# Interface Unit Representation
#
# vlan: 	VLAN ID
# ip:		Virtual IP Address
# ipreal: 	Local IP Address
# mask:		Subnet Mask

class interface:
	def __init__(self):
		self.vlan = ""
		self.ip = ""
		self.mask = ""
		self.ipreal = ""
	def __str__(self):
		return str(self.vlan) + "\t|" + str(self.ip) + "\t|" + str(self.mask)

# Opens an existing configuration file
f = open("FWL-OLD-CFG.txt","r")
# Sets VRRP priority
prio = "200"
# Sets the interface tracked (typically the trunk interface)
trackedInterface = "ge-0/0/3"
# Stores the results
results = []
# Temporary interface object
temp = interface()

flag = True
for l in f:
	if "vlan-id" in l:
		temp.vlan = l.strip().split(" ")[1][:-1]
		flag = True
	if flag:
		if "address" in l:
			v = l.strip().split(" ")[1].split("/")[0].split(".")[0:3]
			v.append(str(int(l.strip().split(" ")[1].split("/")[0].split(".")[3])-2))
			temp.ipreal = v[0] + "." + v[1] + "." + v[2] + "." + v[3]
			temp.ip = l.strip().split(" ")[1].split("/")[0]
			temp.mask = l.strip().split(" ")[1].split("/")[1][:-1]
		if "}" in l:
			flag = False
			results.append(copy.copy(temp))

for i in results:
	if i.vlan == "":
		print ""
	else:
		print "unit " + i.vlan + " {"
		print "\t" + "vlan-id " + i.vlan + ";"
		print "\tfamily inet {"
		print "\t\taddress " + i.ipreal + "/" + i.mask + ";"
		print "\t\tvrrp-group 1 {"
		print "\t\t\tvirtual-address " + i.ip + ";"
		print "\t\t\tpriority " + prio + ";"
		print "\t\t\tno-preempt;"
		print "\t\t\taccept-data;"
		print "\t\t\ttrack {"
		print "\t\t\t\tinterface " + trackedInterface + " {"
		print "\t\t\t\t\tpriority-cost " + prio + ";"
		print "\t\t\t\t}"
		print "\t\t\t}"
		print "\t\t}"
		print "\t}"
		print "}"