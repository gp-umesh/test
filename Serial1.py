import os
import time
import serial
import datetime

# configure the serial connections (the parameters differs on the device you ar$
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=300,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

while 1 :

    #if input == 'exit':
    #if input == 'exit':
    #    ser.close()
    #    exit()
    out = ''
    ser.write('0xAA' + '\r\n')
    date = datetime.datetime.now()
    print(str(date) + '---> 0xAA')
    # let's wait one second before reading output (let's give device time to an$
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print ">>" + out




