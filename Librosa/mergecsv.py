#!/usr/bin/env python3

from __future__ import print_function
import sys
import numpy as np
import csv

prefix=sys.argv[1]
count=sys.argv[2]

files=[]
for i in np.arange(1,int(count)+1):
	files+=[prefix+'_'+str(i)]
print(files)

headerlist=[]
with open(files[0], newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	headerlist=csvreader.__next__()

out = open(prefix, "w")
csv_out = csv.writer(out, delimiter=',')
csv_out.writerow(headerlist)

for cfile in files:
	print('current file:'+cfile)
	with open(cfile, newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		_headerlist=csvreader.__next__() #skip header
		for row in csvreader:
			csv_out.writerow(row)
