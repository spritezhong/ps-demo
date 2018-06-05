import math
import numpy as np
from sklearn.cross_validation import train_test_split
from workandserver import PWorkerClass
class LRmodel():
	def __init__(self,epochs):
		self.worker = PWorkerClass(2, '127.0.0.1', 8001, 'worker', 0, 1)
		self.worker.register()
		self.worker.waitready()
		self.epochs=epochs
		# self.keylist=[]
		# self.vallist=[]


	def readdata(self,filepath):
		dataMat = []
		labelMat = []
		fr = open(filepath)
		for line in fr.readlines():
			lineArr = line.strip().split()
			dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
			labelMat.append(int(lineArr[2]))
		X = np.mat(dataMat)
		Y = np.mat(labelMat).transpose()
		self.X, self.X_test, self.Y, self.Y_test = train_test_split(X, Y, test_size=0.2, random_state=20)
	def calc_gradient(self,valist):
		val=[]
		for i in valist:
			val.append([i])
		assray_v=np.mat(val)
		s=1/(1+np.exp(self.X*assray_v))
		error=s-self.Y
		grad=self.X.transpose()*error
		print('grad',type(grad))
		gradlist=[]
		gl=grad.tolist()
		for i in range(len(gl)):
			gradlist.append(gl[i][0])
		# for id in sorted(self.dict_v.keys()):
		# 	self.dict_grad[id] = grad[int(id), 0]
		print('list',gradlist)
		return gradlist



	def print(self):
		pass
	def train(self):
		self.keylist=[i for i in range(3)]
		self.vallist=[0]*3
		for i in range(self.epochs):
			self.worker.wait(self.worker.pull(self.keylist, self.vallist))
			print('valist',self.vallist)
			gradlist=self.calc_gradient(self.vallist)
			print('graddddddd',gradlist)
			self.worker.wait(self.worker.push(self.keylist,gradlist,self.print))
		print('over!!!!')


