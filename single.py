#worker与server的基类
import message_pb2 as message
import config
import threading
import time

from zmqsock import ZMQSOCK
from threading import Lock
class CallBack:
    def __init__(self,fun,*arg):
        self.arg=arg
        self.fun=fun


    def run(self):
        self.fun(self.arg)
class SingleClass(object):
	def __init__(self,rank,ip,port,role,client_id,servernum,handle,handle_clock):
		#初始化自己节点信息,后续应该改为直接从配置文件读取
		self.is_recover=config.is_recover
		self.save_path=config.save_path
		self.node=message.Node()
		self.node.rank=rank
		self.node.ip=ip
		self.node.port=port
		self.node.role=role
		self.node.client_id=client_id
		self.connect_ids={}
		self.servernum=servernum
		self.tracker=[]            #每个元素为[sendnum,recnum]
		self.mutex = Lock()
		self.handle=handle  #增加回调函数handle，对于worker来说，执行PWorker.process(),对于server来说执行PServer.process()
		self.handle_clock=handle_clock #从服务端获取是否符合迭代窗口， 只有worker执行该函数，对于server来说为空
		# self.ready=False
		self.zmqs = ZMQSOCK()
		self.zmqs.start()

		#启动线程监听消息

		self.ready = False
		self.heart_thread = threading.Thread(target=self.heartbeat(120))
		self.heart_thread.start()
		self.sendtime=0



	def register(self):
		self.zmqs.bind(self.node)
		print('role:%s register'% self.node.role)
		msg = message.Meta()
		schedule_node=message.Node()
		schedule_node.id=1
		schedule_node.ip='127.0.0.1'
		schedule_node.port=8002
		self.zmqs.connect(schedule_node,self.node)
		msg.control.command = 'add node'
		msg.control.reg_node.ip = self.node.ip
		msg.control.reg_node.port = self.node.port
		msg.control.reg_node.role=self.node.role
		msg.timestamp=self.sendtime
		self.sendtime += 1
		msg.recv_id=schedule_node.id
		self.zmqs.sendmsg(msg)
		self.recieve_thread = threading.Thread(target=self.receiving)
		self.recieve_thread.start()

	def waitready(self):
		while(self.ready==False):
			pass
	def receiving(self):
		while True:
			buf=self.zmqs.recvmsg()
			if	buf.control.command=='tell node':
				nodelists=message.NodeList()
				nodelists.ParseFromString(buf.body)
				for node in nodelists.nodel:
					if node.ip==self.node.ip and node.port==self.node.port:
						self.node.id=node.id
						break
				for node in nodelists.nodel:
					self.zmqs.connect(node,self.node)
				self.ready=True

			elif buf.control.command=='exit':
				self.ready=False
				self.zmqs.stop()
				break
			elif buf.control.command=='ssp':
				self.handle_clock(buf)


			else:
				self.handle(buf)            #处理接收到的消息
				if buf.request==False:    # 记录当前时间戳有一个消息得到回复
					ts=buf.timestamp
					self.mutex.acquire()
					self.tracker[ts][1]+=1
					self.mutex.release()
					# self.recnum[ts]+=1

	def heartbeat(self,interval):           #每隔一段时间向schedule发送消息表示自己还活着
		while(interval>0 and self.ready):
			time.sleep(interval)
			msg=message.Meta()
			msg.control.command='heart'
			msg.recv_id=1
			self.copynode(msg.control.reg_node,self.node)
			msg.timestamp=self.sendtime
			self.sendtime+=1
			self.send(msg)
			# self.send(msg)
	def copynode(self,desnode,srcnode):
		desnode.id=srcnode.id
		desnode.ip=srcnode.ip
		desnode.port=srcnode.port
		desnode.is_recover=srcnode.is_recover
		desnode.role=srcnode.role

	def send(self,msg):
		while(self.ready==False):
			a=1
		self.zmqs.sendmsg(msg)

	'''
		def send(self,msg):             #这里发送消息在已知table_node后根据id查表的
		while(self.ready==False):
			a=1
		print('send')
			# time.sleep(1)
		# ts=msg.timestamp
		recv_id=msg.recv_id
		sock_sender=self.connect_ids[str(recv_id)]
		sock_ip=list(sock_sender.keys())[0]
		sock_port=sock_sender[sock_ip]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((sock_ip,sock_port))
		# info=json.loads(json_string)
		sock.send(msg.SerializePartialToString())
		sock.close()
	'''



	def stop(self):
		lmeta=message.Meta()
		lmeta.control.command='exit'
		lmeta.recv_id=self.node.id
		lmeta.sender_id=self.node.id
		# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock.connect((self.node.ip, self.node.port))
		# self.send(lmeta.SerializePartialToString())
		self.send(lmeta)
		# sock.close()

		self.recieve_thread.join()
		self.heart_thread.join()



	def handle_clock(self):
		pass