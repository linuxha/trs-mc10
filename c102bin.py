#!/usr/bin/python3

import os, sys
import re

# Read in a c10 file, tear out the blocks and write the result to a file
"""
Future optioins to add:
- Read the tape print it's filename
- Allow the command line to override the file name
- save the filename with the .bin extention
- create a <Filename>.txt file with the load and run locations
"""
def sync(d):
    x = 0
    while(d[x] != 0x3C):
        if(x > 256):
            return(-1)
        #
        x += 1
    #

    return x+1
#

help = """c102bin.py file.cas
This will save the file to the filename inside the c10 file
"""

if(len(sys.argv) != 2) :
    # put help here
    print(help, file=sys.stderr)
    exit(-1);
#

fileNom = sys.argv[1];

print("Filenom = %s" % fileNom)

with open(fileNom, 'rb') as data_file:
    data = data_file.read() #.decode('utf8')
#

"""
1st block - sync block  - 128 U's, then <
2nd block - fname block -
nth block - data block  -
"""
oStr = ''
l = len(data)
# Skip the first 128 'U'
x = sync(data)
#print("data[%d]: %s" % (x, data[x]))
#print("128: %s" % (data[129]))

# The block format for Data blocks, Namefile blocks, or an End
# of File block is as follows:
# 
# - 1 - One leader byte  55H
# - 1 - One sync byte  3CH
# - 1 - One block type byte  01H = Data FFH = End of File 00H = Namefile
# - 1 - One block length byte  00H to FFH
# - X - Data  0 to 255 bytes
# - 1 - One checksum byte  the sum of all the data plus block type and block length
# - 1 - One leader byte  55H
#
b = 0

startAddr = 0
loadAddr  = 0
filename  = ""

if(data[x] == 0x00):
    # The Namefile block is a standard block with a length of 15 bytes
    # (0FH) and the block type equals 00H. The 15 bytes of data provide
    # information to BASIC and are employed as described below:
    #
    # - 8 - Eight bytes for the program name
    # - 1 - One file type byte  00H = BASIC 01H = Data 02H = Machine Language
    # - 1 - One ASCII flag byte  00H = Binary FFH = ASCII
    # - 1 - One Gap flag byte  01H = Continuous FFH = Gaps
    # - 2 - Two bytes for the start address of a machine language program
    # - 2 - Two bytes for the load address of a machine language program
    #print("X: %d" % x)
    #print("Data: %s" % (type(data).__name__))
    #print("Data: %s" % (type(data[130:132]).__name__))

    #print("^O (0f) 0x%02X" % (data[131]))
    b = data[131]
    #b = int.from_bytes(data[132], byteorder='big', signed=False )
    #print("^O (0f) 0x%02X" % (b))
    a = x+2
    z = a+8
    filename  = data[a:z].decode('utf8').rstrip()
    a = z+2
    z = a+2
    startAddr = int.from_bytes(data[a:z], byteorder='little', signed=False )
    a = z
    z = a+2
    loadAddr  = int.from_bytes(data[a:z], byteorder='little', signed=False )

    print("Filename: [%s](%d)" % (filename, len(filename)))
    print("Start:    0x%04X" % (startAddr))
    print("Load:     0x%04X" % (loadAddr))
    #
    pass
else:
    print("Ooops")
    exit(1)
#
x += 15
#print("L = %d" % len(data[x:-1]))
#print("L = %d" % (l - x))
x += sync(data[x:])
x -= 2
#print("L = %d" % len(data[x:-1]))
#print("L = %d" % (l - x))
print("d[x] = %02x" % (data[x]))
print("d[x+1] = %02x" % (data[x+1]))
#print("x = %d (280)" % x)

bStr = bytes()
blk  = 1
while x < len(data):
    #
    # The block format for Data blocks, Namefile blocks, or an End
    # of File block is as follows:
    # 
    # - 1 - One leader byte  55H
    # - 1 - One sync byte  3CH
    # - 1 - One block type byte  01H = Data FFH = End of File 00H = Namefile
    # - 1 - One block length byte  00H to FFH
    # - X - Data  0 to 255 bytes
    # - 1 - One checksum byte  the sum of all the data plus block type and block length
    # - 1 - One leader byte  55H
    #
    print("\nBLK # = %d" % blk)
    blk += 1
    #print("MARK  = 0x%02X" % data[x])
    #print("SYNC  = 0x%02X" % data[x+1])
    x += 2 # past the U<
    t = data[x] # block type
    #print("Type  = 0x%02X" % data[x])
    x += 1
    l = data[x] # block length
    t = l
    #print("Len   = 0x%02X (0x%04X)" % (l, x))
    x += 1      # Start of the block data
    l += x      # End data
    #print("X     = 0x%04X # 202\nL = 0x%02X # 537" % (x, l))
    #print("BL    = 0x%02X" % len(data[x:l]))
    bStr += data[x:l] # block data
    #print("Bstr  = 0x%02X" % len(bStr))
    x = l + 2 # l bytes and past the checksum and 'U'
#

# Write the block data to the file
with open(filename, "wb") as wfile:
    wfile.write(bStr)
#

exit(0)

# ------------------------------------------------------------------------------
while(x <= 128):
    pass
#
for i in data:
    if(i >= 0x20 and i <= 0x7E):
       oStr += ("%s") % i
    else:
       oStr += '.'
    #
#
print(len(data))

print(oStr)
