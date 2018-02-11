#!/usr/bin/env python

import csv
import os
import time
import datetime

f = open('test.csv', 'wt')

print csv.list_dialects()

writer = csv.writer(f)

writer.writerow( ('Title1', 'Title2', 'Title3') )
writer.writerow( ('Title1', 'Title2', 'Title3') )

tsU = time.time()
tsS = datetime.datetime.fromtimestamp(tsU).strftime('%Y-%m-%d %H:%M:%S')


myQ = []
myQ.append(tsS)
myQ.append(int(tsU))
myQ.append("Hello")
myQ.append(212)

print myQ
writer.writerow(myQ)

del myQ[:]

tsU = time.time()
tsS = datetime.datetime.fromtimestamp(tsU).strftime('%Y-%m-%d %H:%M:%S')

myQ.append(tsS)
myQ.append(int(tsU))
myQ.append("what?")
myQ.append(718)

print myQ
writer.writerow(myQ)

f.close()

exit()

if os.path.isfile('tmp.txt'):
	os.remove('tmp.txt')
else:
	print "File does not exist!!"
