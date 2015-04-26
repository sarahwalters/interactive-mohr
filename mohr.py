import matplotlib.pyplot as plt
import math
import numpy as np


# PLOTTING 2D STATE OF STRESS

def convert(sigxx, sigyy, tauxy, theta):
    ''' Calculates principal stresses for 2D state of stress. '''

    rad = math.radians(theta)
    sigxxp = (sigxx+sigyy)/2 + (sigxx-sigyy)*math.cos(2*rad)/2 + tauxy*math.sin(2*rad)
    sigyyp = (sigxx+sigyy)/2 - (sigxx-sigyy)*math.cos(2*rad)/2 - tauxy*math.sin(2*rad)  
    tauxyp = -(sigxx-sigyy)*math.sin(2*rad)/2 + tauxy*math.cos(2*rad)

    return [sigxxp, sigyyp, tauxyp]


def plot2d(sigxx, sigyy, tauxy):
    ''' Plots the 2D state of stress. '''

    plt.hold(True)
    for i in range(360):
        [sigxxp, sigyyp, tauxyp] = convert(sigxx, sigyy, tauxy, i)
        plt.plot(sigxxp, tauxyp, 'ro')
        plt.plot(sigyyp, -tauxyp, 'bo')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()


# PLOTTING 3D STATE OF STRESS

def calc_sigp(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz):
    ''' Calculates principal stresses for 3D state of stress. '''

    a = 1
    b = sigxx + sigyy + sigzz
    c = sigxx*sigyy + sigxx*sigzz + sigyy*sigzz - tauxy**2 - tauyz**2 - tauxz**2
    d = sigxx*sigyy*sigzz + 2*tauxy*tauxz*tauyz - sigxx*(tauyz**2) - sigyy*(tauxz**2) - sigzz*(tauxy**2)

    [sigxxp, sigyyp, sigzzp] = np.roots([a, -b, c, -d])

    return [sigxxp, sigyyp, sigzzp]


def find_center(sigp1, sigp2):
    ''' Find the center of a circle. '''

    return (sigp1+sigp2)/2


def find_radius(sigp, center):
    ''' Find the radius of a circle. '''

    return (sigp - center)


def calc_circle(center, radius, theta):
    ''' Calculates circle path given center and radius. '''

    radian = math.radians(theta)
    x = radius * math.cos(radian) + center
    y = radius * math.sin(radian)

    return [x, y]


# def define_circle(sigp1, sigp2):
#     ''' Calculates circle center and radius. '''

#     center = (sigp1 + sigp2)/2

#     return [center]

def plot3d(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz):
    ''' Plots the 3D state of stress. '''

    [sigxxp, sigyyp, sigzzp] = calc_sigp(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz)

    cxy = find_center(sigxxp, sigyyp)
    cxz = find_center(sigxxp, sigzzp)
    cyz = find_center(sigyyp, sigzzp)

    rxy = find_radius(sigxxp, cxy)
    rxz = find_radius(sigxxp, cxz)
    ryz = find_radius(sigyyp, cyz)

    # 
    # [cxy, rxy] = define_circle(sigxxp, sigyyp)
    # [cxz, rxz] = define_circle(sigxxp, sigzzp)
    # [cyz, ryz] = define_circle(sigyyp, sigzzp)
    # 

    plt.hold(True)
    for i in range(360):
        [xval1, yval1] = calc_circle(cxy, rxy, i)
        [xval2, yval2] = calc_circle(cxz, rxz, i)
        [xval3, yval3] = calc_circle(cyz, ryz, i)

        plt.plot(xval1, yval1, 'go')
        plt.plot(xval2, yval2, 'bo')
        plt.plot(xval3, yval3, 'ro')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()