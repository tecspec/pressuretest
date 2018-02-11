#!/usr/bin/env python

import os
import csv
import time
import datetime
import threading
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def openPort():
	global client	
	#client = ModbusClient('10.18.78.222', port=502)
	client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=0.1, dtr=False)
	connection = client.connect()

	client.socket.dtr = 0
	client.socket.rts = 0
	time.sleep(1.5)
	client.socket.flushInput()

def closePort():

	client.close()

def readVolts():	
	result = client.read_holding_registers(8,2,unit=3)
	decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)
	return float(decoder.decode_32bit_uint()) / 1000
		
def readSensor(chan):	
	result = client.read_holding_registers((chan * 2) -2 ,2,unit=3)
	decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)
	return (float(decoder.decode_32bit_uint())-4000)*0.01875

def readSensors():	
	result = client.read_holding_registers(0 ,6,unit=3)
	tsU = int(time.time())

	decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)

	data = []

	data.append(datetime.datetime.fromtimestamp(tsU).strftime('%Y-%m-%d %H:%M:%S'))
	data.append(tsU)

	for i in xrange(3):
		data.append((float(decoder.decode_32bit_uint())-4000)*0.01875)
	return data

def writeRelay(chan, val):
	rq = client.write_register(chan + 73, val, unit=3)

def openValve():
	writeRelay(1,1)
	time.sleep(20)	# wait for valve to open
	writeRelay(1,0)
	time.sleep(25)	# wait for valve to close

def openCSV(fn):
	global f
	global writer
	
	f = open(fn, 'wt')
	writer = csv.writer(f)
	writer.writerow( ('Timestamp', 'UNIX Timestamp', 'Test-set Pressure', 'Input Pressure', 'Temperature') )

def closeCSV():
	f.close()

def delCSV(fn):
	closeCSV()
	if os.path.isfile(fn):
		os.remove(fn)


# ----MAIN----

fileName = 'test.csv'
tLength = 30

openPort()

pTank = readSensor(2)
if pTank < 5:
	print "Pressure too low to begin!!"
	closePort()
	exit()

print "Closing bleed valve!!"
writeRelay(2,1)
time.sleep(15)
print "Test cycle beginning!!"

t = threading.Thread(target=openValve)
t.start()


loopCtl = True
started = False

time.sleep(1)

openCSV(fileName)

while loopCtl:

	time.sleep(1)

	if not t.isAlive() and not started:
		print "TESTING BEGIN"
		pStart = readSensor(1)
		if pStart/pTank > 0.95:
			started = True
			tsStart = time.time()
		else:
			print "Pressure not maintained!!"
			loopCtl = False

	if started:
		data = readSensors() 
		print data[2]	# current pressure
		writer.writerow(data)

		if data[2]/pStart < 0.95:
			print "Test Failed!!"
			failed = True
			delCSV(fileName)
			loopCtl = False

		if data[1] - tsStart > tLength:
			print "Test Passed!!"
			closeCSV()
			loopCtl = False


writeRelay(2,0)	# Open bleed valve

while readSensor(1) > 5:
	time.sleep(1)

print "Complete!!"

closePort()



