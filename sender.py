import os
import serial
import time

s = serial.Serial('/dev/pts/31')
s.flushOutput()

with open('inputfile.txt') as input_file:
    file_name = input_file.name
    file_size = os.path.getsize('inputfile.txt')
    content = input_file.read()

print 'sender starts'
s.write('<<START NIGER>>')
time.sleep(1)

s.write(file_name)
time.sleep(1)

s.write(str(file_size))
time.sleep(1)

s.write(content)
print 'sender finishes'

