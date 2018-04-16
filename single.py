#worker与server的基类
import message_pb2 as message
import socket
import json
import threading
class SingleClass(object):
	def __init__(self,id,ip,port,role,client_id,handle):
		#初始化自己节点信息,后续应该改为直接从配置文件读取
		self.node=message.Node()
		self.node.id=id
		self.node.ip=ip
		self.node.port=port
		self.node.role=role
		self.node.client_id=client_id
		self.connect_ids={}
		self.sendnum=[]            #某时间戳内发送的消息数
		self.recnum=[]              #某时间戳内接受的消息数
		self.handle=handle  #增加回调函数handle，对于worker来说，执行PWorker.process(),对于server来说执行PServer.process()
		self.recieve_thread = threading.Thread(self.recieving)
		#启动线程监听消息
	def receiving(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8001))
		while True:
			connection, address = sock.accept()
			buf = json.loads(connection.recv(2048).decode()) #收到来自schedule的table_node
			if buf.control.command=='tell node':
				self.connect_ids=buf.body
			else:
				self.handle(buf)            #处理接收到的消息
				if buf.request==False:    # 记录当前时间戳有一个消息得到回复
					ts=buf.timestamp
					self.recnum[ts]+=1

	def send(self,msg):
		ts=msg.timestamp
		recv_id=msg.recv_id
		sender_id=msg.sender_id
		sock_sender=self.connect_ids[recv_id]
		sock_ip=list(sock_sender.keys())[0]
		sock_port=sock_sender[sock_ip]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((sock_ip,sock_port))
		json_string = json.dumps(msg)
		# info=json.loads(json_string)
		sock.send(json_string.encode())
		sock.close()

	def stop(self):
		self.recieve_thread.join()



'''
	def process(self,msg):     # PServer与PWorker具体实现此函数
		pass
	def send(self,ip,port,msg): #msg发送到<ip,port>
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
		json_string=json.dumps(msg)
		sock.send(json_string.encode())
		sock.close()


	def request(self):
		self.req_node.cmd=1 #1表示注册信号
		msg=message.Meta()
		msg.rcmd=self.req_node
		self.send(self,'localhost','8002',msg) 		#向schedule发送注册消息

	def run(self):
		pass
'''

class PWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id):
		super(PWorkerClass, self).__init__(id,ip,port,role,client_id,self.process)
		self.dict_callback={}         #<timestamp,callback>
		self.dict_kv={}       #存放每个timestamp的数据信息
	def process(self,msg): #处理从服务器中pull下来的数据
		ts=msg.timestamp
		self.dict_kv[ts]=msg.body
		if self.recnum[ts]==1: #这里应该是等于服务器的数量
			self.run_callback(ts)     #全部返回，执行回调函数

	def add_callback(self,timestamp,callback):
		#这里需要互斥访问self.dict_callback，后期需要引入锁的机制
		self.dict_callback[timestamp]=callback
	def run_callback(self,timestamp):
		if timestamp not in self.dict_callback.keys():
			return
		#这里应该保证操作互斥，后期加锁
		self.dict_callback[timestamp]         #执行回调函数
		del self.dict_callback[timestamp]     #从列表删除
	def push(self,dict_grad,callback): #callback是消息被服务器接受后执行的函数
		server_num=1 #getnum(ServerGroup)与之通信的服务器组内的服务器数量

		#需要进一步完善。。。。。。。。。。。。。
		msg = message.Meta()
		msg.body=json.dumps(dict_grad)
		msg.timestamp=server_num
		msg.request=False
		msg.sender_id=self.node.id
		self.sendnum[msg.timestamp] = server_num
		self.add_callback(msg.timestamp,callback)
		# self.send(ip, port, msg)
		msg.recv_id=8#暂不考虑根据key值，查找对应机器的id
		self.send(msg) #需要根据参数的id，查找对应server的id，发送消息

	def pull(self,dict_w):
		server_num = 1
		msg = message.Meta()
		msg.body = json.dumps(dict_w)
		msg.timestamp = server_num
		msg.request = True
		msg.sender_id = self.node.id
		msg.recv_id = 8  # 暂不考虑根据key值，查找对应机器的id
		self.send(msg)  # 需要根据参数的id，查找对应server的id，发送消息


	def wait(self,timestamp):
		while(self.sendnum[timestamp]!=self.recnum[timestamp]):
			print('wait')


class PServerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,data,handle):
		super(PServerClass, self).__init__(id,ip,port,role,client_id,self.process)
		self.data=data     #存放参数值
		self.handle=handle

	def process(self,msg):
		#本地复制下信息
		lmeta=message.Meta()
		lmeta.body=msg.body
		lmeta.timestamp=msg.timestamp
		lmeta.sender_id=msg.sender_id
		lmeta.recv_id=msg.recv_id
		lmeta.request=msg.request
		#这里应该等待含有改段参数梯度值的worker全部发送数据过来
		if lmeta.request==False:     #表示传来的是push请求
			grad = json.loads(lmeta.body.decode())  # 后续需要改进
			for id in grad.keys():
				if id in self.data.keys():
					self.data[id] -= grad[id]
		else:
			self.response(lmeta)


		##########################


	def response(self,request_msg):
		lmeta=message.Meta()
		lmeta.sender_id=request_msg.recv_id
		lmeta.recv_id=request_msg.sender_id
		lmeta.timestamp=request_msg.timestamp
		lmeta.request=False
		index=request_msg.body.decode()
		re_vals={}
		for key in index.keys():
			if key in self.data.keys():
				re_vals[key]=self.data[key]
		lmeta.body=json.dumps(re_vals).encode()
		#################待完善#############
		#需要添加一个根据节点id查询节点<ip,port>的函数
		self.send(lmeta) #根据request_msg中的节点id，查询节点相应的<ip,port>回复消息



