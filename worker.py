# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:44:15 2020

@author: User
"""


from GaussianGenerator import GaussianGenerator
import numpy as np
import communicator
import sys
import torch
import time


PORT = 1232
PORT2 = 1233
HOSTADDR = "container1"
serv = communicator.Server(PORT)
loc_model = (HOSTADDR, PORT)
loc_server = (HOSTADDR, PORT2)

#get dataset
X, Y = GaussianGenerator(100,100)
x_temp = np.ones((200,1))
X = np.concatenate((x_temp,X),axis = 1)

for j in range(10):
	#send request to server for model w
	msg = "Req"
	serv.send(loc_model, msg)
	print(f"Sent {str(msg)}")

	#wait for model 
	w = serv.recv()
	print(f"Received weights {str(w)}")
	#w = [1,1,1]


	#get sample
	r = np.random.choice(200, 10)
	x = X[r]
	y = Y[r]
	
	#compute gradient
	g = np.array([0,0,0])
	for i in range(10):
		if ((np.dot(w,x[i])>=0 and y[i]==-1) or (np.dot(w,x[i])<0 and y[i]==1)):
			g = g -np.multiply(y[i],x[i])
	
	g = g/10
	print(f"Grad computed is {str(g)}")
	
	#Byzantine behavior
	if (np.random.random_sample()<0.5):
		g = -np.multiply(10,g)
		print(f"Malicious grad is {str(g)}")
	
	#send g to server
	serv.send(loc_server, g)
	time.sleep(3)
