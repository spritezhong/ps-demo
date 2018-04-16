from queue import Queue
from worker import WorkerClass
import threading
import message_pb2 as message
import socket
import json
class ScheduleClass(object):
	def __init__(self,workcount):
		self.state=0                    #启动状态，初始0，表示先启动schedule节点
		self.schedule_node=message.Node()
		self.current_node=message.Node()
		self.connect_ids={}    #<node.id，(ip,port>> #id和通信地址的映射
		# self.__workqueue=Queue.queue()          #装任务的集合
		self.__workers={}                       #<string,thread>集合 每个worker为一个线程
		# self.__dict_results={}                  #存放每个worker的执行结果
		# self.list_node=[]                       #存放所有注册节点的信息。
		self.workcount=workcount

		#从配置文件读取节点信息
	def start(self,client_id):
		#初始化schedule节点信息
		if self.state==0:
			self.schedule_node.id=4                    #机器编号
			self.schedule_node.client_id=client_id       #本地作业编号
			self.schedule_node.ip='local host'
			self.schedule_node.port=8002
			self.schedule_node.role='schedule'
			cmap={self.schedule_node.ip:self.schedule_node.port}
			self.connect_ids[self.schedule_node.id]=cmap    #增加schedule节点信息
			self.recieve_thread=threading.Thread(self.recieving)
			self.state+=1
		#待定：判断当前节点是否为schedule节点，如果不是则向schedule节点发送自身节点消息。
	def stop(self):
		self.recieve_thread.join()


	def recieving(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8002))
		workcount=0
		list_conn=[]
		while True:
			connection, address = sock.accept()
			buf = json.loads(connection.recv(2048).decode())  # 收到来自schedule的table_node
			if buf.control.command=='add node':            #代表是注册信息
				workcount+=1
				list_conn.append(connection)
				reg_node=buf.control.reg_node
				cmap={reg_node.ip:reg_node.port}
				self.connect_ids[reg_node.id]=cmap

			if workcount==self.workcount:  #注册的work已满足要求
				break
		msg=message.Meta()                  #把tabel_node广播给连入的所有节点
		msg.control.command=='tell node'
		msg.body=json.dumps(self.connect_ids)
		for con in list_conn:
			con.send(msg.encode())
			con.close()

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




