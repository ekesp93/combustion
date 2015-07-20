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
pltfile = "data3.xyzb"


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

class Spot(object):
    def __init__(self, x, y, z, p, u, v, w, rho, T, S1, S2, S3, S4, S5, pCount, react, nu_t, nu_x, nu_y, nu_z, EV, NUT):
        self.x = x
        self.y = y
        self.z = z
        self.p = p
        self.u = u
        self.v = v
        self.w = w
        self.rho = rho
        self.T = T
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        self.S4 = S4
        self.S5 = S5
        self.pCount = pCount
        self.react = react
        self.nu_t = nu_t
        self.nu_x = nu_x
        self.nu_y = nu_y
        self.nu_z = nu_z
        self.EV = EV
        self.NUT = NUT

# -------------------------------------------------------------------------------
# CODE
import struct
from random import *
from math import *
import time

file = open(filename1, 'wb')
file2 = open(filename2, 'wb')
file3 = open(csvfile, 'wb')
file4 = open(pltfile, 'wb')
fileread = open("particle00027.vtk", 'r')
pltread = open("movie0028.plt", 'r')
points = []
plt = []
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
                "\",\"" + str(format(points[x].velx, '.16f')) + "\",\"" + str(format(points[x].vely, '.16f')) + "\",\"" +
                str(format(points[x].velz, '.16f')) + "\",\"" + str(format(points[x].vel, '.16f')) + "\"\n")

for x in range(1, 38604):
    temp = pltread.readline()
    if x > 3:
        temp = temp.strip('\n')
        parsed = temp.split(" ")
        if len(parsed) != 1 and parsed[2] != 'ZONE':
            insert = Spot(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            k = 0
            for y in range(0, len(parsed)):
                if parsed[y] != '':
                    if k == 0:
                        insert.x = float(parsed[y])
                    elif k == 1:
                        insert.y = float(parsed[y])
                    elif k == 2:
                        insert.z = float(parsed[y])
                    elif k == 3:
                        insert.p = float(parsed[y])
                    elif k == 4:
                        insert.u = float(parsed[y])
                    elif k == 5:
                        insert.v = float(parsed[y])
                    elif k == 6:
                        insert.w = float(parsed[y])
                    elif k == 7:
                        insert.rho = float(parsed[y])
                    elif k == 8:
                        insert.T = float(parsed[y])
                    k += 1
            temp = pltread.readline()
            temp = temp.strip('\n')
            parsed = temp.split(" ")
            for y in range(0, len(parsed)):
                if parsed[y] != '':
                    if k == 9:
                        insert.S1 = float(parsed[y])
                    elif k == 10:
                        insert.S2 = float(parsed[y])
                    elif k == 11:
                        insert.S3 = float(parsed[y])
                    elif k == 12:
                        insert.S4 = float(parsed[y])
                    elif k == 13:
                        insert.S5 = float(parsed[y])
                    elif k == 14:
                        insert.pCount = float(parsed[y])
                    elif k == 15:
                        insert.react = float(parsed[y])
                    elif k == 16:
                        insert.nu_t = float(parsed[y])
                    elif k == 17:
                        insert.nu_x = float(parsed[y])
                    k += 1
            temp = pltread.readline()
            temp = temp.strip('\n')
            parsed = temp.split(" ")
            for y in range(0, len(parsed)):
                if parsed[y] != '':
                    if k == 18:
                        insert.nu_y = float(parsed[y])
                    elif k == 19:
                        insert.nu_z = float(parsed[y])
                    elif k == 20:
                        insert.EV = float(parsed[y])
                    elif k == 21:
                        insert.NUT = float(parsed[y])
                    k += 1
            plt.append(insert)

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
