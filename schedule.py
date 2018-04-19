# from queue import Queue
# from worker import WorkerClass
import threading
import message_pb2 as message
import socket
import json
import time
class ScheduleClass(object):
	def __init__(self,workcount,is_schedule):
		self.state=0                    #启动状态，初始0，表示先启动schedule节点
		self.schedule_node=message.Node()
		self.current_node=message.Node()
		self.connect_ids={}    #<node.id，(ip,port>> #id和通信地址的映射
		# self.__workqueue=Queue.queue()          #装任务的集合
		self.__workers={}                       #<string,thread>集合 每个worker为一个线程
		# self.__dict_results={}                  #存放每个worker的执行结果
		# self.list_node=[]                       #存放所有注册节点的信息。
		self.workcount=workcount
		self.is_schedule=is_schedule
		self.num_servers=0
		self.num_workers=0
		self.share_node={}         #共享通信地址的worker
		self.list_heart={}        #记录每个节点的上次活跃时间

	def workranktoID(self,rank):
		return rank*2+9
	def serverranktoID(self,rank):
		return rank*2+8

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




	def recieving(self):
		# print('recieving')
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8002))
		workcount=0

		sock.listen()
		while True:
			connection, address = sock.accept()
			buf=message.Meta()
			info=connection.recv(2048)
			buf.ParseFromString(info)
			# buf = json.loads(connection.recv(2048).decode())  # 收到来自schedule的table_node
			# print('buf:%s' %buf)
			time_add=time.time()
			if buf.control.command=='add node':            #代表是注册信息
				workcount+=1
				reg_node=buf.control.reg_node
				cmap={reg_node.ip:reg_node.port}
				conflict_flag=False
				if reg_node.role=='worker':
					reg_node.id=self.workranktoID(self.num_workers)
					self.num_workers+=1
				elif reg_node.role=='server':
					reg_node.id=self.serverranktoID(self.num_servers)
					self.num_servers+=1
				for key in self.connect_ids.keys():
					if self.connect_ids[key]==cmap:
						conflict_flag=True
						break
				if conflict_flag:
					self.share_node[reg_node.id]=cmap
				self.connect_ids[reg_node.id]=cmap

				#更新节点的活跃时间
				self.update_heart(reg_node.id,time.time())
				if (self.num_servers + self.num_workers)==self.workcount:  # 注册的work已满足要求
					msg = message.Meta()  # 把tabel_node广播给连入的所有节点
					msg.control.command = 'tell node'
					msg.body = json.dumps(self.connect_ids).encode()
					# msg.body=json.dumps(self.connect_ids)
					print("send to worker")
					self.sendtoall(msg)
			elif buf.control.command=='heart':
				self.update_heart(buf.control.reg_node.id, time.time())



				# break
			 #如果有复活节点存在，把复活节点告知给其它节点
			# wait_time=time.time()     #如果一段时间内注册节点的数量都不满足要求，则认为有节点已经死亡
			# if wait_time-time_add>internal:
			# 	dropdeadnode

		# for con in list_conn:
		# 	con.send(msg.SerializePartialToString())
		# 	con.close()

	def sendtoall(self,msg):

		for key in self.connect_ids.keys():
			if key==4:continue
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ip=list(self.connect_ids[key].keys())[0]
			port=self.connect_ids[key][ip]
			address=(ip,port)
			print('send to all')
			print(address)
			sock.connect(address)
			sock.send(msg.SerializePartialToString())
			sock.close()


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




