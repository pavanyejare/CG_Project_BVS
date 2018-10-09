#!/usr/bin/python 

import serial
import time
ser = serial.Serial('/dev/ttyS0')
header = [0xef,0x01,0xff,0xff,0xff,0xff]
def setBaud():
    ser.baudrate = 57600


img2tz = {0:"generate character file complete",
          1:"error while reciving packet",
          0x06:"fail to generate character file due to the over-distorterly fingerprint image",
          0x07:"failed to generate characterfile due to lackness of character or point or over smallness of the fingerprint image",
          0x15:"fail to0 generate image file for the lackness of valid primary image."}


def write():
    setBaud()
    data = [0xef, 0x01, 0xff, 0xff, 0xff, 0xff, 0x01, 0x00, 0x03, 0x01, 0x00, 0x05]
    ###############  Finger Collection in Image Buffer #############
    print "Scan Finger First time"    
    while 1:
     ser.write(bytearray(data));
     time.sleep(0.5)
     s = ser.read(ser.inWaiting())
     id = int(ord(s[9]))
     if( id == 0):
        break
    print([hex(ord(c)) for c in s])
    finger_status = {0:"finger collection successs",1:"error when receiving package",2:"cant detect finger",3:"fail to collect finger"}
    print (finger_status[int(ord(s[9]))]) 
    #####       Generate Character file from image buffer   Img2Tz      ############
    data = header + [0x01,0x00,0x04,0x02,0x01,0x00,0x08]
    ser.write(bytearray(data));
    time.sleep(1)
    recived = ser.read(ser.inWaiting())
    print ([hex(ord(c)) for c in recived]) 
    print (img2tz[int(ord(recived[9]))])  
    ######################
    #____________________________________________________________________________________#
    #####           Scan Same Finger Secon time and Stroe in charbuffer 2 ###########
    print "#******************************************************************#"
    print "Scan Same Finger Second Time"
    data = [0xef, 0x01, 0xff, 0xff, 0xff, 0xff, 0x01, 0x00, 0x03, 0x01, 0x00, 0x05]
    while 1:
     ser.write(bytearray(data));
     time.sleep(0.5)
     s = ser.read(ser.inWaiting())
     id = int(ord(s[9]))
     if( id == 0):
        break
    print([hex(ord(c)) for c in s])
    print (finger_status[int(ord(s[9]))])
    #####       Generate Character 2 file from image buffer   Img2Tz      ############
    data = header + [0x01,0x00,0x04,0x02,0x02,0x00,0x09]
    ser.write(bytearray(data));
    time.sleep(1)
    recived = ser.read(ser.inWaiting())
    print ([hex(ord(c)) for c in recived])
    print (img2tz[int(ord(recived[9]))])
    #___________________________________________________________________________________#

    # -------------      To generate template RegModel  -------------------------------#
    data = header +[0x01, 0x00, 0x03, 0x05, 0x00, 0x09]
    ser.write(bytearray(data));
    time.sleep(1)
    recive = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in recive])
    regmodel = {0:"operation success",1:"error while reciving packet",0x0a:"failed to combine character files"}
    print (regmodel[int(ord(recived[9]))])
    # ----------------------------- End regmodel --------------------------#
    
    ## ---------------- Read valid template number TempleteNum  ------------------------- #
    data = header +[0x01, 0x00, 0x03, 0x1d, 0x00, 0x21]
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    templetnum = {0:"read complete.",1:"error while reciving package."}
    print (templetnum[int(ord(s[9]))])
    num = s[10:12]
    temp = 256*ord(num[0]) + ord(num[1])
    print "Recived Temple : ", str(temp)
    # -------------------------  End Templete Num -------------- # 

    # ---------------- To store template Store   ----------------- # 
    tno = int(temp)+1
    data1 = [0x01, 0x00, 0x06, 0x06, 0x01, tno/100, tno%100]
    csum = sum(data1)
    cs1 = csum/100
    cs2 = csum%100
    data = header +[0x01, 0x00, 0x06, 0x06, 0x01, tno/100, tno%100, cs1, cs2]
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    print len(s)
    store = {0:"storage success",1:"error while reciving packet",0x0b:"addressing PageId is beyond the finger library.",
             0x18:"error while writing flash."}
    print (store[int(ord(s[9]))])
    status = (store[int(ord(s[9]))])
    return (tno, status)
    # ---------------- End Store   ------------------------------------- #
     
    

