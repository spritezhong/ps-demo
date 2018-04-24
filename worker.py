import socket
import numpy as np
import json
from sklearn.cross_validation import train_test_split
import logging
import logging.config

from queue import Queue

class WorkerClass(object):
    def __init__(self,list_id,fuc,num): #v表示向量的维度
        self.X=[]
        self.Y=[]
        self.X_test=[]
        self.Y_test=[]
        self.dict_v={}
        self.dict_grad={}
        self.dict_info={}
        # self.__work_queue=Queue.Queue()
        self.__works={}
        self.__dict_result={}
        for i in list_id:
            self.dict_info[i]=0
        self.dict_info['type']='pull'
        self.handle=fuc
        self.param=num
    def H(self):
        self.handle(2)
    def set_workqueue(self,workqueue):
        self.__work_queue=workqueue
    def set_result(self,result):
        self.__dict_result=result
    def run(self):             #worker端工作流程
        while(True):
            if self.__work_queue.empty(): break
            task=self.__work_queue.get()
            #handle(task)             #task需要定义
    def read_data(self,filepath):
        dataMat=[];labelMat=[]
        fr=open(filepath)
        for line in fr.readlines():
            lineArr=line.strip().split()
            dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
            labelMat.append(int(lineArr[2]))
        # print(np.mat(dataMat).shape)
        X=np.mat(dataMat)
        Y=np.mat(labelMat).transpose()
        self.X,self.X_test,self.Y,self.Y_test=train_test_split(X,Y,test_size=0.2,random_state=20)




        #load_data

    def pull(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('localhost',8001))
        self.dict_info['type']='pull'
        # print('worker')
        # print(self.dict_info)
        json_string=json.dumps(self.dict_info)
        sock.send(json_string.encode())
        # print('已发送')
        ss=sock.recv(2048).decode()
        # print('recieve weight:%s'%ss)
        self.dict_v=json.loads(ss)
        sock.close()

        #通过socket向服务器发送命令'pull’+data
        #服务器解析收到的指令，发送参数给客户端
        #客户端接收到参数值
    def calc_gradient(self):
        #为方便计算，把self.dict_v转变为(size(),1)的array
        list_v=[]
        for id in sorted(self.dict_v.keys()):
            list_v.append([self.dict_v[id]])
        asraay_v=np.mat(list_v)
        s=1/(1+np.exp(self.X*asraay_v))
        error=s-self.Y
        grad=self.X.transpose()*error
        for id in sorted(self.dict_v.keys()):
            self.dict_grad[id]=grad[int(id),0]
    def push(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8001))
        self.dict_grad['type']='push'
        json_string = json.dumps(self.dict_grad)
        sock.send(json_string.encode())
        # sock.send(('push').encode())
        sock.close()
         #通过socket向服务器发送命令'push’+data
    def calc_pre(self,X,W):
        s = 1 / (1 + np.exp(sum(X * W)))
        if s > 0.5:
            return 1.0;
        else:
            return 0.0

    def predict(self):
        list_w = []
        print(self.dict_v)
        for id in sorted(self.dict_v.keys()):
            list_w.append([self.dict_v[id]])
        weight = np.mat(list_w)
        m,n=self.X_test.shape
        # pre=0
        loss=0
        for i in range(m):
            pre=self.calc_pre(self.X_test[i],weight)
            if int(pre)!=int(self.Y_test[i]):
                loss+=1
        error_rate=float(loss)/m
        print("error rate is: %f" %error_rate)

            # s=1/(1+np.exp(sum(self.X_test[i]*weight)))
            # if s>0.5:pre=1
            # else: pre=0
        # s = 1 / (1 + np.exp(self.X * weight))
        # print(sum(s))
        # print(type(s))
        # error = s - self.Y
list_function={}
# list_arg={}
def func(num):
    num+=1
    print('hello')
    print(num)
def addcallback(ts,function):
    list_function[ts]=function
    # list_arg[ts]=arg

if __name__=='__main__':
    a=1
    print('a',a)
    log_filename = "logging.log"
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filemode='a')
    if a==1:
        logging.error('erroe')
    # addcallback(0,func,)
    # list_function[0](list_arg[0])
    # work=WorkerClass([0,1,2],{print('hello')})
    # work.H()

