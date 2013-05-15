# Author: 	Gregory A. Lussier
# Subject:	OSPF Interface Configuration Generation
#
# Description:
# Generates passive interfaces statements for every VLANs.

config = open("FWL-OLD-CFG.txt","r")

vlan = []
for line in config:
	if "vlan-id" in line:
		line = line.strip()
		line = line.split(" ")
		line = line[1].replace(";","")
		vlan.append(line)

for v in vlan:
	print "Ge-0/0/3." + v + " {" + "\n" + "\tpassive;" + "\n}"