#!/usr/bin/env python

#import string

inp = raw_input("Input to change: ")

print inp

startPos = inp.find("`b2")

print startPos
endPos = inp.find("`",startPos+1)

print endPos

print inp.lstrip("`b2")
print inp[startPos+3:endPos]
