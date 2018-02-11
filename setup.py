#!/usr/bin/env python

import time
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#client = ModbusClient('10.18.78.222', port=502)
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=0.1, dtr=False)
connection = client.connect()

client.socket.dtr = 0
client.socket.rts = 0
time.sleep(1.5)
client.socket.flushInput()

result = client.read_holding_registers(59,1,unit=3)
print result.registers[0]


client.close()
exit()

result = client.read_holding_registers(64,8,unit=3)
print result.registers

inp_num = raw_input("Input to change: ")
inp_mode = raw_input("New Mode: ")

rq = client.write_register(63+int(inp_num), int(inp_mode), unit=3)

result = client.read_holding_registers(64,8,unit=3)
print result.registers


client.close()

