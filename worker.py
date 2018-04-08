import socket
import math
import numpy as np
import json
class WorkerClass(object):
    def __init__(self,list_id): #v表示向量的维度
        self.X=[]
        self.Y=[]
        self.dict_v={}
        self.dict_grad={}
        self.dict_info={}
        for i in list_id:
            self.dict_info[i]=0
        self.dict_info['type']='pull'


    def read_data(self,filepath):
        dataMat=[];labelMat=[]
        fr=open(filepath)
        for line in fr.readlines():
            lineArr=line.strip().split()
            dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
            labelMat.append(int(lineArr[2]))
        X=dataMat
        Y=labelMat
        print(X[2])
        print(Y[2])

        #load_data

    def pull(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('localhost',8001))
        self.dict_info['type']='pull'
        print(self.dict_info)
        json_string=json.dumps(self.dict_info)
        sock.send(json_string.encode())
        self.dict_v=json.loads(sock.recv(2048).decode())
        sock.close()

        #通过socket向服务器发送命令'pull’+data
        #服务器解析收到的指令，发送参数给客户端
        #客户端接收到参数值
    def calc_gradient(self):
        #为方便计算，把self.dict_v转变为(size(),1)的array
        list_v=[]
        for id in sorted(self.dict_v.keys()):
            list_v.append([self.dict_v[id]])
        print(list_v)
        asraay_v=np.array(list_v)
        s=1/(1+math.exp(self.X*list_v))
        error=s-self.Y
        grad=self.X.transpose()*error
        for id in sorted(self.dict_v.keys()):
            self.dict_grad[id]=grad[id,0]
    def push(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8001))
        self.dict_grad['type']='push'
        json_string = json.dumps(self.dict_grad)
        sock.send(json_string.encode())
        # sock.send(('push').encode())
        sock.close()
         #通过socket向服务器发送命令'push’+data
    def predict(self):
        print(self.dict_v)

