# Writes a sample point cloud to use with the example pointcloud reader
# -------------------------------------------------------------------------------
# CONFIGURATION
scale = 10

# point cloud extent (x,z) in blocks (scale*scale meters)
extx = 10
extz = 10

# point cloud density in each block (blocks are scale*scale meters)
density = 500

# output file name
filename1 = "data.xyzb"
filename2 = "data2.xyzb"
csvfile = "data.csv"


class Point(object):
    def __init__(self, x, y, z, temp, velx, vely, velz, vel):
        self.x = x
        self.y = y
        self.z = z
        self.temp = temp
        self.velx = velx
        self.vely = vely
        self.velz = velz
        self.vel = vel

# -------------------------------------------------------------------------------
# CODE
import struct
from random import *
from math import *
import time

file = open(filename1, 'wb')
file2 = open(filename2, 'wb')
file3 = open(csvfile, 'wb')
fileread = open("particle00027.vtk", 'r')
points = []
maxTemp = 0
maxVel = 0

file3.write("x,y,z,temp,velx,vely,velz,vel\n")

for x in range(1, 960450):
    temp = fileread.readline()
    if x > 9 and x < 68610:
        parsed = temp.split(" ")
        points.append(Point(float(parsed[6]), float(parsed[12]), float(parsed[18]), 0.0, 0.0, 0.0, 0.0, 0.0))
    elif x > 68613 and x < 137214:
        parsed = temp.split(" ")
        points[x - 68614].temp = float(parsed[6])
    elif x > 891848 and x < 960449:
        parsed = temp.split(" ")
        k = 0
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                if k == 0:
                    points[x - 891849].velx = float(parsed[y])
                elif k == 1:
                    points[x - 891849].vely = float(parsed[y])
                elif k == 2:
                    points[x - 891849].velz = float(parsed[y])
                k += 1
                points[x - 891849].vel = math.sqrt(math.pow(points[x - 891849].velx, 2) +
                                                math.pow(points[x - 891849].vely, 2) +
                                                math.pow(points[x - 891849].velz, 2))

for x in range(0, len(points)):
    if points[x].temp > maxTemp:
        maxTemp = points[x].temp
    if points[x].velx > maxVel:
        maxVel = points[x].velx
    file3.write("\"" + str(points[x].x) + "\",\"" + str(points[x].y) + "\",\"" + str(points[x].z) + "\",\"" + str(points[x].temp) +
                "\",\"" + str(points[x].velx) + "\",\"" + str(points[x].vely) + "\",\"" + str(points[x].velz) + "\",\"" +
                str(points[x].vel) + "\"\n")

def generatePoint1(x, y, z, temp):
    # generate plane with RGBA data values all set to 1.
    r = temp/maxTemp
    g = 0.0
    b = (maxTemp - temp)/maxTemp
    return struct.pack('ddddddd', x, y, z, r, g, b, 1.0)

def generatePoint2(x, y, z, vel):
    r = vel/maxVel
    g = (maxVel - vel)/maxVel
    b = 0.0
    return struct.pack('ddddddd', x, y, z, r, g, b, 1.0)

def outputBlock(x, z):
    for fx in range(0, len(points)):
        px = points[fx].x
        py = points[fx].y
        pz = points[fx].z
        temp = points[fx].temp
        vel = points[fx].vel
        dataBytes = generatePoint1(px, py, pz, temp)
        file.write(dataBytes)
        dataBytes = generatePoint2(px, py, pz, vel)
        file2.write(dataBytes)

# generate and output line by line
for x in range(0, extx):
    print("row {0}".format(x))
    for z in range(0, extz):
        outputBlock(x, z)

file.close()
file2.close()

totPointsK = extx * extz * density * density / 1000
print("total points: {0}K".format(totPointsK))
