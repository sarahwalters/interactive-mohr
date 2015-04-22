import matplotlib.pyplot as plt
import math

def convert(sigxx, sigyy, tauxy, theta):
	rad = math.radians(theta)
	sigxxp = (sigxx+sigyy)/2 + (sigxx-sigyy)*math.cos(2*rad)/2 + tauxy*math.sin(2*rad)
	sigyyp = (sigxx+sigyy)/2 - (sigxx-sigyy)*math.cos(2*rad)/2 - tauxy*math.sin(2*rad)	
	tauxyp = -(sigxx-sigyy)*math.sin(2*rad)/2 + tauxy*math.cos(2*rad)

	return [sigxxp, sigyyp, tauxyp]

def plot(sigxx, sigyy, tauxy):
	plt.hold(True)
	for i in range(360):
		[sigxxp, sigyyp, tauxyp] = convert(sigxx, sigyy, tauxy, i)
		plt.plot(sigxxp, tauxyp, 'ro')
		plt.plot(sigyyp, -tauxyp, 'bo')

	plt.gca().set_aspect('equal', adjustable='box')
	plt.draw()
	plt.show()