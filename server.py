import numpy as np
import random
import json
import socket
class ServerClass(object):

    def __init__(self,alpha,list_id):
        self.alpha=alpha

        self.dict_w={}
        for i in list_id:
            self.dict_w[i]=random.random()
        #模块初始化
    def update(self,buf):
        for id in self.dict_w.keys():
            if(id=='type'):continue
            self.dict_w[id]-=self.alpha*buf[id]
    def  process(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('localhost',8001))
        sock.listen(5)
        while True:
            connection,address=sock.accept()
            # try:
            if True:
                # connection.settimeout(5)
                # print('connect')
                buf=json.loads(connection.recv(2048).decode())
                # print('server')
                # print(buf)
                if buf['type']=='pull':
                    #后期追加根据buf里面的feature_id获取dict_w里面的相关参数
                    json_string = json.dumps(self.dict_w)
                    # print("send weight:%s" %json_string)
                    connection.send(json_string.encode())
                else:
                    for id in buf.keys():
                        if(id=='type'):
                            continue

                        self.dict_w[int(id)]-=self.alpha*buf[id]
                        # print('update weight: %s' %self.dict_w)
            # except:
            else:
                print('error')


if __name__ == '__main__':
    serve=ServerClass(0.001,[0,1,2])
    serve.process()
