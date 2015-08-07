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
    def __init__(self, x, y, z, temp, nu, omega, S1, S2, S3, S4, S5, weight, nu_x, nu_y, nu_z, velx, vely, velz, vel):
        self.x = x
        self.y = y
        self.z = z
        self.temp = temp
        self.nu = nu
        self.omega = omega
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        self.S4 = S4
        self.S5 = S5
        self.weight = weight
        self.nu_x = nu_x
        self.nu_y = nu_y
        self.nu_z = nu_z
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
import math
import time

file = open(filename1, 'wb')
file2 = open(filename2, 'wb')
file3 = open(csvfile, 'wb')
file4 = open(pltfile, 'wb')
fileread = open("particle00007.vtk", 'r')
pltread = open("movie0028.plt", 'r')
points = []
plt = []
maxTemp = 0
maxVel = 0
maxP = 0
maxCount = 0
count = 0

file3.write("x,y,z,temp,velx,vely,velz,vel\n")

i = 0
for x in range(1,10):
    temp = fileread.readline()
    if x == 9:
        parsed = temp.split(" ")
        for y in range(0, len(parsed)):
            if parsed[y] != '' and parsed[y] != 'POINTS' and parsed[y] != 'float\n':
                maxCount = int(parsed[y])
for x in range(10, maxCount * 14):
    temp = fileread.readline()
    parsed = temp.split(" ")
    if i == 0: # X Y Z coordinates
        points.append(Point(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        k = 0
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                if k == 0:
                    points[count].x = float(parsed[y])
                elif k == 1:
                    points[count].y = float(parsed[y])
                elif k == 2:
                    points[count].z = float(parsed[y])
                k += 1
        count += 1
    elif i == 1 and parsed[0] == '': # Temperature
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].temp = float(parsed[y])
        count += 1
    elif i == 2 and parsed[0] == '': # nu_t
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].nu = float(parsed[y])
        count += 1
    elif i == 3 and parsed[0] == '': # Omega
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].omega = float(parsed[y])
        count += 1
    elif i == 4 and parsed[0] == '': # Scalar 1
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].S1 = float(parsed[y])
        count += 1
    elif i == 5 and parsed[0] == '': # Scalar 2
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].S2 = float(parsed[y])
        count += 1
    elif i == 6 and parsed[0] == '': # Scalar 3
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].S3 = float(parsed[y])
        count += 1
    elif i == 7 and parsed[0] == '': # Scalar 4
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].S4 = float(parsed[y])
        count += 1
    elif i == 8 and parsed[0] == '': # Scalar 5
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].S5 = float(parsed[y])
        count += 1
    elif i == 9 and parsed[0] == '': # Weight
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].weight = float(parsed[y])
        count += 1
    elif i == 10 and parsed[0] == '': # nu_x
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].nu_x = float(parsed[y])
        count += 1
    elif i == 11 and parsed[0] == '': # nu_y
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].nu_y = float(parsed[y])
        count += 1
    elif i == 12 and parsed[0] == '': # nu_z
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                points[count].nu_z = float(parsed[y])
        count += 1
    elif i == 13 and parsed[0] == '': # Velocity
        k = 0
        for y in range(0, len(parsed)):
            if parsed[y] != '':
                if k == 0:
                    points[count].velx = float(parsed[y])
                elif k == 1:
                    points[count].vely = float(parsed[y])
                elif k == 2:
                    points[count].velz = float(parsed[y])
                k += 1
                points[count].vel = math.sqrt(math.pow(points[count].velx, 2) +
                                              math.pow(points[count].vely, 2) +
                                              math.pow(points[count].velz, 2))
        count += 1
    if count == maxCount:
        i += 1
        count = 0
        temp = fileread.readline()

for x in range(0, len(points)):
    if points[x].temp > maxTemp:
        maxTemp = points[x].temp
    if points[x].vel > maxVel:
        maxVel = points[x].vel
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

for x in range(0, len(plt)):
    if plt[x].p > maxP:
        maxP = plt[x].p

def generatePoint1(x, y, z, temp):
    # generate plane with RGBA data values all set to 1.
    r = 1.0
    g = (maxTemp - temp)/maxTemp
    b = (maxTemp - temp)/maxTemp
    return struct.pack('ddddddd', x, y, z, r, g, b, 1.0)

def generatePoint2(x, y, z, vel):
    r = (maxVel - vel)/maxVel
    g = 1.0
    b = (maxVel - vel)/maxVel
    return struct.pack('ddddddd', x, y, z, r, g, b, 1.0)

def generatePoint3(x, y, z, p):
    r = (maxP - p)/maxP
    g = (maxP - p)/maxP
    b = 1.0
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
    for fx in range(0, len(plt)):
        px = plt[fx].x
        py = plt[fx].y
        pz = plt[fx].z
        p = plt[fx].p
        dataBytes = generatePoint3(px, py, pz, p)
        file4.write(dataBytes)

# generate and output line by line
for x in range(0, extx):
    print("row {0}".format(x))
    for z in range(0, extz):
        outputBlock(x, z)

file.close()
file2.close()

totPointsK = extx * extz * density * density / 1000
print("total points: {0}K".format(totPointsK))
