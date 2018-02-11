#!/usr/bin/env python

import logging
import time
import requests
#from time import strftime
import datetime
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
#from pymodbus.payload import BinaryPayloadBuilder
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#client = ModbusClient('10.18.78.222', port=502)
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=0.1, dtr=False)
connection = client.connect()

client.socket.dtr = 0
client.socket.rts = 0
time.sleep(1.5)
client.socket.flushInput()

url = "https://emoncms.org/input/post.json"

result = client.read_holding_registers(0,8,unit=3)
tsU = time.time()

decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)
p1 = (float(decoder.decode_32bit_uint())-4000)*0.01875
p2 = (float(decoder.decode_32bit_uint())-4000)*0.01875
t1 = (float(decoder.decode_32bit_uint())-4000)*0.01875
t2 = (float(decoder.decode_32bit_uint())-4000)*0.01875

tsS = datetime.datetime.fromtimestamp(tsU).strftime('%Y-%m-%d %H:%M:%S')

dStr = tsS + "," + str(tsU) + ","
oStr = str(p1) + ","
oStr = oStr + str(p2) + ","
oStr = oStr + str(t1) + ","
oStr = oStr + str(t2)

print dStr + oStr

data = {'node':'20','csv':oStr,'apikey':'7216d36181130681895cbb4c5fe73e66'}
r = requests.post(url,params=data)


client.close()
exit()

dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","
dStr = dStr + str(float(decoder.decode_32bit_int()) / 10000) + ","


result = client.read_holding_registers(152,2,unit=0x01)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)

dStr = dStr + str(decoder.decode_32bit_int() / 1000.0) + ","


result = client.read_holding_registers(184,4,unit=0x01)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)

dStr = dStr + str(decoder.decode_32bit_int()) + ","
dStr = dStr + str(decoder.decode_32bit_int())


url = "https://emoncms.org/input/post.json"
data = {'node':'20','csv':dStr,'apikey':'7216d36181130681895cbb4c5fe73e66'}
r = requests.post(url,params=data)
print r

#print dStr

client.close()
