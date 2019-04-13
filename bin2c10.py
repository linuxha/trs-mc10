#!/usr/bin/python

# -*- coding: latin-1 -*-
import os
import re
import sys

def hexvl(a_st):
    a_st  = a_st.lower()
    tmpr  = 0
    hx_st = "0123456789abcdef"
    hx_st = hx_st.lower()

    for i in range(0,len(a_st),1):
        tmpr=(tmpr*16)+hx_st.find(a_st[i])
    #

    return tmpr
#

def help():
    print("bin2cas - 201012221554 - Paulo Silva (GPL license)")
    print("converts a binary file into a CoCo2 .cas file")
    print("usage: bin2cas.py file.bin CAS_NAME address")
    print("the result will be a file named: file.cas")
    print("This converter based on information from:\nhttp://www.cs.unc.edu/~yakowenk/coco/text/tapeformat.html")
    exit(1)
#

#
try:
    if(len(sys.argv) != 4):
        print("Incorrect number of arguements")
        help()
    #
    if(re.search('.bin$', sys.argv[1]) == None):
        print("Filename: %s does not end .bin" % (sys.argv[1]))
        help()
    #
    binFile = sys.argv[1]
    print(binFile)
    casFile = sys.argv[1].split('.')[0] + ".cas"
    casName = sys.argv[2]
    addr    = sys.argv[3]
    # strip it of .bin
    #casFile = binFile + ".cas"
except Exception as err:
    print("Exception: %s (%d)" % (err, len(sys.argv)))
    help()
#

if binFile.lower() == "--help".lower():
    help()
else:
  finp_fl = open(binFile,"r");
  fout_fl = open(casFile,"w")

  lfl     = os.path.getsize(binFile) # lfl=lof(1)

  ###
  ### Leader
  ###
  for i in range(0, 128):   #- 0x55 byte synchronism, 128 times...
      fout_fl.write(chr(0x55))
  #

  fout_fl.write(chr(0x55))    #- two "magic bytes"

  fout_fl.write(chr(0x3C))
  fout_fl.write(chr(0x00))    #- block type: filename
  fout_fl.write(chr(0x0F))    #- data lenght

  # (??? - what is this?)
  infnam_st = "ABCDEFGH"
  infnam_st = infnam_st+"        "
  infnam_st = infnam_st[:8]     #- filename - 8 characters
  
  infnam_st = casName.upper()
  print('Filename: "%s"' % (infnam_st))

  for i in infnam_st:
    fout_fl.write(i)
    #fout_fl.write(infnam_st[i])
  #

  fout_fl.write(chr(0x02)) #- machine code
  fout_fl.write(chr(0x00)) #- ascii flag: binary
  fout_fl.write(chr(0x00)) #- gap flag
  fout_fl.write(chr(0x0C)) #- machine code starting address
  fout_fl.write(chr(0x00))
  fout_fl.write(chr(0x0C)) #- machine code loading address
  fout_fl.write(chr(0x00))
  fout_fl.write(chr(0x4D)) #- checksum (bitwiseand 255)
  fout_fl.write(chr(0x55)) #- "magic byte"

  for i in range(0,128,1): #- 0x55 byte synchronism, 128 times...
    fout_fl.write(chr(0x55))
  #

  ###
  ### 
  ###
  while True:
      if lfl < 0:
          break
      #

      fout_fl.write(chr(0x55)) #- two "magic bytes"
      fout_fl.write(chr(0x3C))
      fout_fl.write(chr(0x01)) #- block type: data

      rlf = 0xFF

      if lfl < rlf:
          rlf = lfl
      #

      #print rlf
      fout_fl.write(chr(rlf))  #- data lenght
      cfl = 255
      if lfl < 255:
          cfl = lfl
      #
      cksm=cfl+1
      for i in range(0, 255):
          byte_st = finp_fl.read(1)
          if len(byte_st)==0:
              break
          #
          u    = ord(byte_st)
          cksm = (cksm+u)%256 #- cksm=(cksm+u) mod 256
          fout_fl.write(chr(u)) #- writing byte
      #
      fout_fl.write(chr(cksm)) #- writing checksum
      lfl = lfl - 255
  # while True:

  fout_fl.write(chr(0x55)) #- "magic byte"
  fout_fl.write(chr(0x55)) #- two "magic bytes"
  fout_fl.write(chr(0x3C))
  fout_fl.write(chr(0xFF)) #- eof
  fout_fl.write(chr(0x00)) #- data lenght
  fout_fl.write(chr(0xFF)) #- checksum
  fout_fl.write(chr(0x55)) #- "magic byte"
  finp_fl.close()
  fout_fl.close()
#
