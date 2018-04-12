from queue import Queue
from worker import WorkerClass
import threading
import message_pb2 as message
import socket
import json
class ScheduleClass(object):
	def __init__(self,workcount):
		self.__workqueue=Queue.queue()          #装任务的集合
		self.__workers={}                       #<string,thread>集合 每个worker为一个线程
		# self.__dict_results={}                  #存放每个worker的执行结果
		self.list_node=[]                       #存放所有注册节点的信息。
		self.workcount=workcount
		h_node=message.Node()  #这里应该从配置文件读取节点信息
		h_node.id=1
		h_node.ip='local host'
		h_node.port=8002
		h_node.role='schedule'
		h_node.is_recover=0
		self.list_node.append(h_node)

	def recieve(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 8002))
		workcount=0
		list_conn=[]
		while True:
			connection, address = sock.accept()
			buf = json.loads(connection.recv(2048).decode())  # 收到来自schedule的table_node
			if buf.rcmd.cmd == 1:
				workcount+=1
				list_conn.append(connection)
				self.list_node=buf.rcmd.reg_node

			if workcount==self.workcount:  #注册的work已满足要求
				break
		msg=message.Meta()                  #把tabel_node广播给连入的所有节点
		msg.rcmd.cmd=2
		msg.body=json.dumps(self.list_node)
		for con in list_conn:
			con.send(msg.encode())
			con.close()


	def get_ready(self,ready):
		if(ready==True):
			#分配任务，
			# WorkerClass.set_workqueue(self.__workqueue)
			for i in range(self.workcount):
				self.__workers['W' + i] = threading.Thread(WorkerClass)




	def execute(self):  #启动worker
		for key in self.__workers.keys():
			self.__workers[key].start()

	def isfinished(self): #判断worker是否活跃
		for key in self.__workers.keys():
			if self.__workers[key].is_alive():
				return False
		return True




