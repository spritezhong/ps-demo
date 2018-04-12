#worker与server的基类
import message_pb2 as message
import socket
import json
class SingleClass(object):
	def __init__(self,id,ip,port,role):
		#初始化自己节点信息,后续应该改为直接从配置文件读取
		self.node=message.Node()
		self.node.id=id
		self.node.ip=ip
		self.node.port=port
		self.node.role=role
		self.req_node=message.rcmd()
		self.req_node.reg_node=self.node
		self.list_node={} #存放id通讯列表
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

	def receive(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8002))
		while True:
			connection, address = sock.accept()
			buf = json.loads(connection.recv(2048).decode()) #收到来自schedule的table_node
			if buf.Requestcmd.cmd==2:
				self.list_node=buf.body.decode()
				break
		sock.close()

	def run(self):
		pass
class PWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role):
		super(PWorkerClass, self).__init__(id,ip,port,role)

	def push(self,dict_grad):
		server_num=1 #getnum(ServerGroup)与之通信的服务器组内的服务器数量
		#需要进一步完善。。。。。。。。。。。。。
		msg = message.Meta()
		msg.body=json.dumps(dict_grad)
		msg.timestamp=server_num
		# self.send(ip, port, msg)
		self.send('localhost',8001,msg) #需要根据参数的id，查找对应server的id，发送消息

	def pull(self,dict_w):
		pass
		# server_num=1 #getnum(ServerGroup)与之通信的服务器组内的服务器数量
		# #需要进一步完善。。。。。。。。。。。。。
		# msg = message.Meta()
		# msg.body=json.dumps(dict_w)
		# msg.timestamp=server_num
		# # self.send(ip, port, msg)
		# self.send('localhost',8001,msg) #需要根据参数的id，查找对应server的id，发送消息
class PServerClass(SingleClass):
	def __init__(self,id,ip,port,role,data):
		super(PServerClass, self).__init__(id,ip,port,role)
		self.data=data                    #存放参数值
	def process(self,msg):
		#本地复制下信息
		lmeta=message.Meta()
		lmeta.rcmd=msg.rcmd
		lmeta.body=msg.body
		lmeta.timestamp=msg.timestamp
		lmeta.connectid=msg.connectid
		#这里应该等待含有改段参数梯度值的worker全部发送数据过来

		##########################
		grad=json.loads(lmeta.body.decode()) #后续需要改进
		for id in grad.keys():
			if id in self.data.keys():
				self.data[id]-=grad[id]

	def response(self,request_msg,return_vals):
		lmeta=message.Meta()
		lmeta.rcmd=request_msg.rcmd
		lmeta.timestamp=request_msg.timestamp
		lmeta.body=return_vals
		#################待完善#############
		#需要添加一个根据节点id查询节点<ip,port>的函数
		self.send(ip,port,lmeta) #根据request_msg中的节点id，查询节点相应的<ip,port>回复消息



