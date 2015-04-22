import matplotlib.pyplot as plt
import math
import numpy as np

def convert(sigxx, sigyy, tauxy, theta):
	rad = math.radians(theta)
	sigxxp = (sigxx+sigyy)/2 + (sigxx-sigyy)*math.cos(2*rad)/2 + tauxy*math.sin(2*rad)
	sigyyp = (sigxx+sigyy)/2 - (sigxx-sigyy)*math.cos(2*rad)/2 - tauxy*math.sin(2*rad)	
	tauxyp = -(sigxx-sigyy)*math.sin(2*rad)/2 + tauxy*math.cos(2*rad)

	return [sigxxp, sigyyp, tauxyp]


def plot3d(sigxx, sigyy, sigzz, tauxy, tauxz, tauyz):

	plt.hold(True)
	for i in range(360):
		[sigxxp1, sigyyp1, tauxyp] = convert(sigxx, sigyy, tauxy, i)
		[sigxxp2, sigzzp1, tauxzp] = convert(sigxx, sigzz, tauxz, i)
		[sigyyp2, sigzzp2, tauyzp] = convert(sigyy, sigzz, tauyz, i)

		plt.plot(sigxxp1, tauxyp, 'ro')
		plt.plot(sigyyp1, -tauxyp, 'ro')

		plt.plot(sigxxp2, tauxzp, 'bo')
		plt.plot(sigzzp1, -tauxzp, 'bo')

		plt.plot(sigyyp2, tauyzp, 'go')
		plt.plot(sigzzp2, -tauyzp, 'go')

	plt.gca().set_aspect('equal', adjustable='box')
	plt.draw()
	plt.show()


def plot(sigxx, sigyy, tauxy):
	plt.hold(True)
	for i in range(360):
		[sigxxp, sigyyp, tauxyp] = convert(sigxx, sigyy, tauxy, i)
		plt.plot(sigxxp, tauxyp, 'ro')
		plt.plot(sigyyp, -tauxyp, 'bo')

	plt.gca().set_aspect('equal', adjustable='box')
	plt.draw()
	plt.show()