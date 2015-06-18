# Writes a sample point cloud to use with the example pointcloud reader
#-------------------------------------------------------------------------------
# CONFIGURATION
scale = 10

# point cloud extent (x,z) in blocks (scale*scale meters)
extx = 10
extz = 10

# point cloud density in each block (blocks are scale*scale meters)
density = 500

# output file name
filename = "data.xyzb"

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

#-------------------------------------------------------------------------------
# CODE
import struct
from random import *
from math import *
file = open(filename, 'wb')
fileread = open("particle00027.vtk", 'r')
points = []

for x in range(1, 70000):
    temp = fileread.readline()
    if x > 9:
        if temp == "\n":
            break
        else:
            parsed = temp.split(" ")
            points.append(Point(float(parsed[6]), float(parsed[12]), float(parsed[18])))

def generatePoint(x, y, z):
    # generate plane with RGBA data values all set to 1.
    hfy  = 0.5 + ((sin(x*4)) * cos(z) * cos(x)) / 2
    r = 0.5 + (sin(x/4) + cos(z/4)) / 2
    g = (hfy + r) / 2
    b = 1 - r
    return struct.pack('ddddddd', x, y, z, r, g, b, 1.0)

def outputBlock(x, z):
    for fx in range(0, len(points)):
        px = points[fx].x
        py = points[fx].y
        pz = points[fx].z
        dataBytes = generatePoint(px, py, pz)
        file.write(dataBytes)

# generate and output line by line
for x in range(0, extx):
    print("row {0}".format(x))
    for z in range(0, extz):
        outputBlock(x, z)

file.close()


totPointsK = extx*extz*density*density/1000
print("total points: {0}K".format(totPointsK))