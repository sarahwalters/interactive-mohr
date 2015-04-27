import matplotlib.pyplot as plt
import math
import numpy as np


# PLOTTING 2D STATE OF STRESS

def convert(sx, sy, txy, theta):
    ''' Calculates principal stresses for 2D state of stress. '''

    rad = math.radians(theta)
    sxp = (sx+sy)/2 + (sx-sy)*math.cos(2*rad)/2 + txy*math.sin(2*rad)
    syp = (sx+sy)/2 - (sx-sy)*math.cos(2*rad)/2 - txy*math.sin(2*rad)
    txyp = -(sx-sy)*math.sin(2*rad)/2 + txy*math.cos(2*rad)

    return [sxp, syp, txyp]


def plot2d(sx, sy, txy):
    ''' Plots the 2D state of stress. '''

    plt.hold(True)
    for i in range(360):
        [sxp, syp, txyp] = convert(sx, sy, txy, i)
        plt.plot(sxp, txyp, 'ro')
        plt.plot(syp, -txyp, 'bo')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()


# PLOTTING 3D STATE OF STRESS

def calc_sigp(sx, sy, sz, txy, tyz, txz):
    ''' Calculates principal stresses for 3D state of stress. '''

    a = 1
    b = sx + sy + sz
    c = sx*sy + sx*sz + sy*sz - txy**2 - tyz**2 - txz**2
    d = sx*sy*sz + 2*txy*txz*tyz - sx*(tyz**2) - sy*(txz**2) - sz*(txy**2)

    [sxp, syp, szp] = np.roots([a, -b, c, -d])

    return [sxp, syp, szp]


def define_circle(sigp1, sigp2):
    ''' Calculates circle center and radius. '''

    center = (sigp1 + sigp2)/2
    radius = abs(sigp1 - center)

    return [center, radius]


def calc_circle(center, radius, theta):
    ''' Calculates circle path given center and radius. '''

    radian = math.radians(theta)
    x = radius * math.cos(radian) + center
    y = radius * math.sin(radian)

    return [x, y]


def plot3d(sx, sy, sz, txy, txz, tyz):
    ''' Plots the 3D state of stress. '''

    [sxp, syp, szp] = calc_sigp(sx, sy, sz, txy, txz, tyz)

    [cxy, rxy] = define_circle(sxp, syp)
    [cxz, rxz] = define_circle(sxp, szp)
    [cyz, ryz] = define_circle(syp, szp)

    plt.hold(True)
    for i in range(360):
        [xval1, yval1] = calc_circle(cxy, rxy, i)
        [xval2, yval2] = calc_circle(cxz, rxz, i)
        [xval3, yval3] = calc_circle(cyz, ryz, i)

        plt.plot(xval1, yval1, 'go')
        plt.plot(xval2, yval2, 'bo')
        plt.plot(xval3, yval3, 'ro')

    plt.plot(sx, txy, 'ro')
    plt.plot(sx, -txy, 'ro')
    #plt.plot(sx, txz, 'ro')
    plt.plot(sy, txy, 'ro')
    plt.plot(sy, -txy, 'ro')
    #plt.plot(sy, tyz, 'ro')
    #plt.plot(sz, tyz, 'ro')
    #plt.plot(sz, txz, 'ro')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()
