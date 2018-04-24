# from queue import Queue
# from worker import WorkerClass
import threading
import message_pb2 as message
import socket
import json
import time
import datetime
import logging
import logging.config
import config
class ScheduleClass(object):
	def __init__(self,workcount,is_schedule):
		self.state=0                    #启动状态，初始0，表示先启动schedule节点
		self.schedule_node=message.Node()
		self.current_node=message.Node()
		self.connect_ids={}    #<node.id，(ip,port>> #id和通信地址的映射
		# self.__workqueue=Queue.queue()          #装任务的集合
		self.__workers={}                       #<string,thread>集合 每个worker为一个线程
		self.workcount=workcount
		self.is_schedule=is_schedule
		self.num_servers=0
		self.num_workers=0
		self.share_node={}         #共享通信地址的worker
		self.list_heart={}        #记录每个节点的上次活跃时间
		self.heartbeat_timeout=60        #60s内没有动态的认为改节点已死亡
		# log_filename = "schedule.log"
		logging.basicConfig(level=logging.DEBUG,
							format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
							datefmt='%Y-%m-%d %H:%M:%S',
							filemode='a')



		#从配置文件读取节点信息
	def start(self,client_id):
		#初始化schedule节点信息
		if self.state==0:
			self.schedule_node.id=1                    #机器编号
			self.schedule_node.client_id=client_id       #本地作业编号
			self.schedule_node.ip='localhost'
			self.schedule_node.port=8002
			self.schedule_node.role='schedule'
			cmap={self.schedule_node.ip:self.schedule_node.port}
			self.connect_ids[self.schedule_node.id]=cmap    #增加schedule节点信息
			self.recieve_thread=threading.Thread(target=self.recieving)
			self.recieve_thread.start()

			self.state+=1
			'''
					if self.is_schedule==False:
			# self.current_node.id=2
			self.current_node.ip='local host'
			self.current_node.port=8001
			msg=message.Meta()
			msg.control.command='add node'
			# msg.control.reg_node.id=self.current_node.id
			msg.control.reg_node.ip=self.current_node.ip
			msg.control.reg_node.port= self.current_node.port
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(('localhost', 8002)) #这个地址目前是默认已知的
			# print('msg:%s'%msg)
			sock.send(msg.SerializePartialToString())
			sock.close()
		#待定：判断当前节点是否为schedule节点，如果不是则向schedule节点发送自身节点消息。
			'''
	def update_heart(self,id,t):
		self.list_heart[id]=t

	def stop(self):
		self.recieve_thread.join()

	def getdeadnode(self,t):
		curtime=datetime.datetime.now()
		# print(curtime)
		dead_nodes=[]
		print('listheart')
		print(self.list_heart)
		for key in self.list_heart.keys():
			delta=curtime-self.list_heart[key]
			if delta.seconds>t:
				dead_nodes.append([key])
		return dead_nodes

	def updatenodeinfo(self,deadnodes,node):
		recovernode=message.Node()
		recovernode.id=-1
		if node in deadnodes.keys() :  #这个node是不知道自己id的，从原来注册的信息表里获取自己的id，rank
			for key in self.connect_ids.keys():
				cmap=list[self.connect_ids[key].keys()]
				if node.ip==cmap[0] and node.port==cmap[1]:
					node.id=key
					node.rank=config.IDtorank(node.id)
					recovernode=node
					break
		if recovernode.id==-1:
			logging.error('no recover node')
		msg=message.Meta()
		msg.sender_id=self.schedule_node.id
		msg.recv_id=recovernode.id
		msg.body=json.dumps(self.connect_ids).encode()
		msg.control.command='tell node'
		self.send(msg) #将节点信息列表告知给复活节点



	def recieving(self):
		# print('recieving')
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8002))
		workcount=0
		recovernodes=[]
		sock.listen()
		while True:
			connection, address = sock.accept()
			buf=message.Meta()
			info=connection.recv(2048)
			buf.ParseFromString(info)
			# buf = json.loads(connection.recv(2048).decode())  # 收到来自schedule的table_node
			# print('buf:%s' %buf)
			if buf.control.command=='add node':            #代表是注册信息
				deadnodes=self.getdeadnode(self.heartbeat_timeout)
				workcount+=1
				reg_node=buf.control.reg_node
				cmap={reg_node.ip:reg_node.port}
				conflict_flag=False
				if reg_node.role=='worker':
					reg_node.id=config.workranktoID(self.num_workers)
					self.num_workers+=1
				elif reg_node.role=='server':
					reg_node.id=config.serverranktoID(self.num_servers)
					self.num_servers+=1
				for key in self.connect_ids.keys():
					if self.connect_ids[key]==cmap:
						conflict_flag=True
						break
				if conflict_flag:
					self.share_node[reg_node.id]=cmap
				self.connect_ids[reg_node.id]=cmap

				#更新节点的活跃时间
				# self.update_heart(reg_node.id,datetime.datetime.now())
				if (self.num_servers + self.num_workers)==self.workcount:  # 注册的work已满足要求
					msg = message.Meta()  # 把tabel_node广播给连入的所有节点
					msg.control.command = 'tell node'
					msg.body = json.dumps(self.connect_ids).encode()
					# msg.body=json.dumps(self.connect_ids)
					print("send to worker")
					self.sendtoall(msg)
				elif (self.num_servers + self.num_workers)>self.workcount: #有死亡节点已经复活
					pass
					# self.updatenodeinfo(deadnodes,reg_node)############

			elif buf.control.command=='heart':
				print('recieve heart id:%s' %buf.control.reg_node.id)
				self.update_heart(buf.control.reg_node.id, datetime.datetime.now())


	def send(self,msg):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		nodeid=msg.recv_id
		ip = list(self.connect_ids[nodeid].keys())[0]
		port = self.connect_ids[nodeid][ip]
		address = (ip, port)
		sock.connect(address)
		sock.send(msg.SerializePartialToString())
		sock.close()

	def sendtoall(self,msg):

		for key in self.connect_ids.keys():
			if key==4:continue
			msg.recv_id=key
			self.send(msg)
			# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# ip=list(self.connect_ids[key].keys())[0]
			# port=self.connect_ids[key][ip]
			# address=(ip,port)
			# print('send to all')
			# print(address)
			# sock.connect(address)
			# sock.send(msg.SerializePartialToString())
			# sock.close()


	#
	# def get_ready(self,ready):
	# 	if(ready==True):
	# 		#分配任务，
	# 		# WorkerClass.set_workqueue(self.__workqueue)
	# 		for i in range(self.workcount):
	# 			self.__workers['W' + i] = threading.Thread(WorkerClass)
	#
	#
	#
	#
	# def execute(self):  #启动worker
	# 	for key in self.__workers.keys():
	# 		self.__workers[key].start()
	#
	# def isfinished(self): #判断worker是否活跃
	# 	for key in self.__workers.keys():
	# 		if self.__workers[key].is_alive():
	# 			return False
	# 	return True




