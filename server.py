# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:53:50 2020

@author: Konstantina
"""

from GaussianGenerator import GaussianGenerator
import numpy as np
import threading
import communicator
import matplotlib.pyplot as plt

PORT = 1232
serv_model = communicator.Server(PORT)
PORT2 = 1233
serv_grad = communicator.Server(PORT2)


w = np.array([0.0,0.0,0.0])

def model_server():
	print("model server thread is up")
	global w
	while True:
		result = serv_model.recv()
		#print(f"Received obj of type {str(type(result))} and content:\n{str(result)}")
		
		#send weights
		serv_model.reply(w, PORT)
		#print(f"Sent obj of type {str(type(w))} and content:\n{str(w)}")



maxit = 1000
k = 10
ns = 10
gamma = 0.1
epsilon = 0.1
rho = 0.002

X, Y = GaussianGenerator(100,100)
x_temp = np.ones((200,1))
X = np.concatenate((x_temp,X),axis = 1)



step = 0

th = threading.Thread(target=model_server, daemon=True)
th.start()

while (step <= 1000):
	if (step%k==0):
		#updater
		r = np.random.choice(200, ns)
		x = X[r]
		y = Y[r]
		#print(f"The sample is {str(x)} with labels {str(y)}")

		v = np.array([0,0,0])
		for i in range(ns):
			if ((np.dot(w,x[i])>=0 and y[i]==-1) or (np.dot(w,x[i])<0 and y[i]==1)):
				v = v -np.multiply(y[i],x[i])
				#print(f"There was a misclassification, new grad is {str(v)}")
		
		v = v/ns
		print(f"Grad from updater is {str(v)}")

	while True:
		#receive g
		g_tilde = serv_grad.recv()
		print(f"Received gradient {str(g_tilde)}")
		if (np.linalg.norm(g_tilde)!= 0):
			c = np.linalg.norm(v)/np.linalg.norm(g_tilde)
			g = [c*e for e in g_tilde]
		else:
			g = g_tilde
		if (gamma*np.dot(v,g)-rho*(np.linalg.norm(g)**2)>=-gamma*epsilon):
			break
		else:
			print("Rejected gradient\n")

	u_g = np.array([gamma*e for e in g])
	w = w - u_g
	print(f"New weights are {str(w)}")


	fig = plt.figure()
	plt.plot(X[:100,1], X[:100,2], 'x')
	plt.plot(X[100:,1], X[100:,2], '*')
	z1 = np.linspace(-6,6,100)
	z2 = - w[1]/w[2]*z1 - w[0]/w[2]
	plt.plot(z1, z2, '-r')
	name = "gaussian"+str(step)+".png"
	plt.savefig(name)
	fig.clf()

	step += 1