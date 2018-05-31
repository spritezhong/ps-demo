# from queue import Queue
# from worker import WorkerClass
import threading
import message_pb2 as message
import datetime
import logging
import logging.config
import config
from zmqsock import ZMQSOCK
import json
class ScheduleClass(object):
	def __init__(self,workcount,is_schedule,staleness):
		self.state=0                    #启动状态，初始0，表示先启动schedule节点
		self.schedule_node=message.Node()
		self.current_node=message.Node()
		self.connect_ids={}    #<node.id，(ip,port>> #id和通信地址的映射 为了方便后续判断是否是恢复节点
		self.__workers={}                       #<string,thread>集合 每个worker为一个线程
		self.workcount=workcount
		self.is_schedule=is_schedule
		self.num_servers=0
		self.num_workers=0
		self.share_node={}         #共享通信地址的worker
		self.list_heart={}        #记录每个节点的上次活跃时间
		self.heartbeat_timeout=60        #60s内没有动态的认为改节点已死亡
		self.min_clock = 0  # 用于ssp的时间机制记录全局最小clock
		self.staleness = staleness
		self.dict_clock=0            #记录当前拥有最小clock的workid
		self.nodes_list=message.NodeList()
		self.zmqs = ZMQSOCK()
		self.zmqs.start()
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
			self.schedule_node.ip='127.0.0.1'
			self.schedule_node.port=8002
			self.schedule_node.role='schedule'
			self.zmqs.bind(self.schedule_node)
			self.zmqs.connect(self.schedule_node,self.schedule_node)
			cmap={self.schedule_node.ip:self.schedule_node.port}
			self.connect_ids[self.schedule_node.id]=cmap    #增加schedule节点信息
			self.recieve_thread=threading.Thread(target=self.recieving)
			self.recieve_thread.start()
			self.state+=1
	def update_heart(self,id,t):
		self.list_heart[id]=t

	def stop(self):

		self.recieve_thread.join()

	def getdeadnode(self,t):
		curtime=datetime.datetime.now()
		dead_nodes=[]
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
		msg.body=self.nodes_list.SerializePartialToString()
		msg.control.command='tell node'
		self.zmqs.sendmsg(msg)
		# self.send(msg) #将节点信息列表告知给复活节点

	def uplocalinfo(self):
		pass

	def add_registernode(self,reg_node):

		cmap = {reg_node.ip: reg_node.port}
		if reg_node.role == 'worker':
			reg_node.id = config.workranktoID(self.num_workers)
			self.num_workers += 1
		elif reg_node.role == 'server':
			reg_node.id = config.serverranktoID(self.num_servers)
			self.num_servers += 1
		cregnode = self.nodes_list.nodel.add()
		self.copynode(cregnode, reg_node)
		conflict_flag = False
		for key in self.connect_ids.keys():
			if self.connect_ids[key] == cmap:
				conflict_flag = True
				break
		if conflict_flag:
			self.share_node[reg_node.id] = cmap
		self.connect_ids[reg_node.id] = cmap
		self.zmqs.connect(reg_node, self.schedule_node)
		# 更新节点的活跃时间
		self.update_heart(reg_node.id, datetime.datetime.now())
		if(self.num_servers + self.num_workers)==self.workcount:
			msg = message.Meta()  # 把tabel_node广播给连入的所有节点
			msg.control.command = 'tell node'
			msg.body=self.nodes_list.SerializePartialToString()
			self.sendtoall(msg)


	def recieving(self):
		# workcount=0
		while True:
			buf=self.zmqs.recvmsg()
			if buf.control.command=='add node':            #代表是注册信息
				deadnodes=self.getdeadnode(self.heartbeat_timeout)
				reg_node=buf.control.reg_node
				if (self.num_servers + self.num_workers) < self.workcount:
					self.add_registernode(reg_node)
				else: #有节点重启
					self.updatenodeinfo(deadnodes, reg_node)
			elif buf.control.command=='ssp':
				sender_id=buf.sender_id
				ts=buf.timestamp
				stale=json.loads(buf.body.decode())
				self.process_clock(stale,sender_id,ts)
			elif buf.control.command=='heart':
				# print('recieve heart id:%s' %buf.control.reg_node.id)
				self.update_heart(buf.control.reg_node.id, datetime.datetime.now())
			elif buf.control.command=='exit':
				self.zmqs.stop()
				break


	def sendtoall(self,msg):

		for key in self.connect_ids.keys():
			if key==self.schedule_node.id:continue
			msg.recv_id=key
			self.zmqs.sendmsg(msg)

	def copynode(self, desnode, srcnode):
		desnode.id = srcnode.id
		desnode.ip = srcnode.ip
		desnode.port = srcnode.port
		desnode.is_recover = srcnode.is_recover
		desnode.role = srcnode.role


	def stop(self):
		lmeta=message.Meta()
		lmeta.control.command='exit'
		lmeta.recv_id=self.schedule_node.id
		lmeta.sender_id=self.schedule_node.id
		self.zmqs.sendmsg(lmeta)
		self.recieve_thread.join()
		# self.heart_thread.join()


	def isuniquemin(self, stale):

		count = 0
		for key in self.dict_clock.keys():
			if self.dict_clock[key] == stale:
				count += 1
		if count == 1:
			return True
		return False

	def getre_clock(self, stale, workid): #锁是不是加的过长了

		self.mutex.acquire()
		if (self.dict_clock.size() == 0):
			self.min_clock = stale
			reflag=True
		elif (stale > self.min_clock + self.staleness):
			reflag=False
		elif (stale == self.min_clock):
			if (self.isuniquemin(stale)):
				self.min_clock += 1
			self.dict_clock[workid] = stale
			reflag=True
		self.mutex.acquire()
		return reflag
	def process_clock(self,stale,workid,ts):
		msg=message.Meta()
		msg.sender_id=self.schedule_node.id
		msg.recv_id=workid
		msg.body=self.getre_clock(stale,workid).encode()
		msg.cmd='ssp'
		msg.timestamp=ts
		self.zmqs.sendmsg(msg)


