import matplotlib.pyplot as plt
import math
import numpy as np


def convert(sigxx, sigyy, tauxy, theta):
    ''' Calculates principal stresses for 2D state of stress. '''

    rad = math.radians(theta)
    sigxxp = (sigxx+sigyy)/2 + (sigxx-sigyy)*math.cos(2*rad)/2 + tauxy*math.sin(2*rad)
    sigyyp = (sigxx+sigyy)/2 - (sigxx-sigyy)*math.cos(2*rad)/2 - tauxy*math.sin(2*rad)  
    tauxyp = -(sigxx-sigyy)*math.sin(2*rad)/2 + tauxy*math.cos(2*rad)

    return [sigxxp, sigyyp, tauxyp]


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


def find_radius():
    ''' Find the radius of a circle. '''


def plot(sigxx, sigyy, tauxy):
    ''' Plots the 2D state of stress. '''

    plt.hold(True)
    for i in range(360):
        [sigxxp, sigyyp, tauxyp] = convert(sigxx, sigyy, tauxy, i)
        plt.plot(sigxxp, tauxyp, 'ro')
        plt.plot(sigyyp, -tauxyp, 'bo')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()


def plot3d(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz):
    ''' Plots the 3D state of stress. '''

    # plot(sigxx, sigyy, tauxy)

    [sigxxp, sigyyp, sigzzp] = calc_sigp(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz)

    cxy = find_center(sigxxp, sigyyp)
    cxz = find_center(sigxxp, sigzzp)
    cyz = find_center(sigyyp, sigzzp)

    # return cxy

    return [cxy, cxz, cyz]
    # cxz
    # cyz

    # plt.hold(True)
    # for i in range(360):
    #     [sigxxp1, sigyyp1, tauxyp] = convert(sigxx, sigyy, tauxy, i)
    #     [xval1, yval1] = convert_other(sigxxp1, sigxx, sigzz, i)
    #     [xval2 , yval2] = convert_other(sigyyp1, sigyy, sigzz, i)

    #     plt.plot(sigxxp1, tauxyp, 'ro')
    #     plt.plot(sigyyp1, -tauxyp, 'ro')

    #     plt.plot(xval1, yval1, 'go')

    #     plt.plot(xval2, yval2, 'bo')

    # print sigxxp1
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.draw()
    # plt.show()
