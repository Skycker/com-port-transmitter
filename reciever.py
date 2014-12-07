import serial
import time

s = serial.Serial('/dev/pts/30', timeout=0.5)
s.flushInput()
print 'port ready'

while True:
    k = s.readline()
    print k
    try:
        print k[-1], '<--'
    except:
        pass
    print len(k)
    if k == '<<START NIGER>>':
        break


time.sleep(1)
file_name = s.readline()
print 'file name recieved %s' % file_name

file_size = s.readline()
time.sleep(1)
print 'file size recieved %s' % file_size

content = ''.join(s.readlines())

print 'transmition ready'
output_file = open('out.txt', 'w')
output_file.write(content)
output_file.close()
print 'file ready'
