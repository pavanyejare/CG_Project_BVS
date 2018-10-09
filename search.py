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

    #--------------------       Generate Character file from image buffer   Img2Tz  -----------------------------#
    data = header + [0x01,0x00,0x04,0x02,0x01,0x00,0x08]
    ser.write(bytearray(data));
    time.sleep(1)
    recived = ser.read(ser.inWaiting())
    print ([hex(ord(c)) for c in recived]) 
    print (img2tz[int(ord(recived[9]))])  
    #--------------------- End Img2Tz ------------------------------#

    # -------------      To search finger library Search (buffer =1 )       -------------------------------#
    data1 = [0x01, 0x00, 0x08 ,0x04, 0x01]
    startpage = 0x0000
    pageno = 0x0064
    p1 = startpage/100
    p2 = startpage%100
    pn1 = pageno / 100
    pn2 = pageno % 100
    csum = sum(data1+[p1, p2, pn1, pn2])
    csum1 = csum / 100
    csum2 = csum % 100
    data = header +[0x01, 0x00, 0x08, 0x04, 0x01, p1, p2, pn1, pn2, csum1, csum2]
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    search = {0:"Found Matching Finger", 1:"error while reciving packet", 0x09:"No Matching in the Library"}
    print (search[int(ord(s[9]))])
    status =  (search[int(ord(s[9]))])
    ack =  int(ord(s[9]))
    if( int(ord(s[9])) == 0 ):
      id1 = int(ord(s[10]))
      id2 = int(ord(s[11]))
      id = id1 | id2
      print  "Page Id : ",id
    #return(status)
    return(status, id, ack)
    # ----------------------------- End Search --------------------------#
    
     
    
#if __name__ == '__main__':
#    write()

