# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:18:10 2020

It generates two 2-d Gaussian distributions with labels 1 and -1.

@author: Konstantina
"""
import numpy as np
import matplotlib.pyplot as plt

def GaussianGenerator (n1, n2):
	mean1 = [3, 6]
	cov1 = [[1,0], [0,1]]
	x1 = np.random.multivariate_normal(mean1,cov1, n1)
	y1 = np.ones(n1)
	
	mean2 = [-1,0]
	cov2 = [[2,0],[0,2]]
	x2 = np.random.multivariate_normal(mean2,cov2, n2)
	y2 = -np.ones(n2)
	
	plt.plot(x1[:,0], x1[:,1], 'x')
	plt.plot(x2[:,0], x2[:,1], '*')
	#plt.show()
	plt.savefig("gaussian.png")
	

	X = np.concatenate((x1,x2), axis = 0)
	Y = np.concatenate((y1,y2), axis = 0)
	return X,Y
