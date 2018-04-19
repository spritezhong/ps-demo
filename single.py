#worker与server的基类
import message_pb2 as message
import socket
import json
import threading
import time
class SingleClass(object):
	def __init__(self,id,ip,port,role,client_id,servernum,handle):
		#初始化自己节点信息,后续应该改为直接从配置文件读取
		self.node=message.Node()
		self.node.id=id
		self.node.ip=ip
		self.node.port=port
		self.node.role=role
		self.node.client_id=client_id
		self.connect_ids={}
		self.servernum=servernum
		# self.sendnum=[]            #某时间戳内发送的消息数
		# self.recnum=[]              #某时间戳内接受的消息数
		self.tracker=[]            #每个元素为[sendnum,recnum]
		self.handle=handle  #增加回调函数handle，对于worker来说，执行PWorker.process(),对于server来说执行PServer.process()
		# self.ready=False
		self.recieve_thread = threading.Thread(target=self.receiving)
		self.recieve_thread.start()
		#启动线程监听消息
		self.ready = False
		self.sendtime=0


	def register(self):
		msg = message.Meta()
		msg.control.command = 'add node'
		# msg.control.reg_node.id = self.node.id
		msg.control.reg_node.ip = self.node.ip
		msg.control.reg_node.port = self.node.port
		msg.control.reg_node.role=self.node.role
		msg.timestamp=self.sendtime
		self.sendtime += 1
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('localhost', 8002))  # 这个地址目前是默认已知的
		sock.send(msg.SerializePartialToString())
		sock.close()
		print('register')
	def receiving(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.node.ip,self.node.port))
		# sock.bind(('localhost', 8001))
		sock.listen()
		while True:
			# print('ddddddd')
			connection, address = sock.accept()
			buf=message.Meta()
			buf.ParseFromString(connection.recv(2048))
			# print('has recieve：%s'%buf)
			# buf = json.loads(connection.recv(2048).decode()) #收到来自schedule的table_node
			if buf.control.command=='tell node':
				self.connect_ids=json.loads(buf.body.decode())
				self.ready=True
				heart_thread=threading.Thread(target=self.heartbeat(5))
				heart_thread.start()
			elif buf.control.command=='exit':
				break
				# id=buf.control.reg_node.id
				# ip=buf.control.reg_node.ip
				# port=buf.control.reg_node.port
				# print('ip:%s'%ip)
				# self.connect_ids[id]={ip:port}
			else:
				self.handle(buf)            #处理接收到的消息
				if buf.request==False:    # 记录当前时间戳有一个消息得到回复
					ts=buf.timestamp
					self.tracker[ts][1]+=1
					# self.recnum[ts]+=1

	def heartbeat(self,interval):           #每隔一段时间向schedule发送消息表示自己还活着
		while(interval>0 and self.ready):
			time.sleep(interval)
			msg=message.Meta()
			msg.control.command='heart'
			msg.recv_id=1
			msg.control.reg_node=self.node
			msg.timestamp=self.sendtime
			self.sendtime+=1
			self.send(msg)


	def send(self,msg):             #这里发送消息在已知table_node后根据id查表的
		while(self.ready==False):
			#这里应该wait
			a=1
		# ts=msg.timestamp
		recv_id=msg.recv_id

		# sender_id=msg.sender_id
		# print('node tables')
		# print(self.connect_ids)
		sock_sender=self.connect_ids[str(recv_id)]
		# print('sock sender')
		# print(sock_sender)
		sock_ip=list(sock_sender.keys())[0]
		sock_port=sock_sender[sock_ip]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((sock_ip,sock_port))
		# info=json.loads(json_string)
		sock.send(msg.SerializePartialToString())
		sock.close()

	def stop(self):
		lmeta=message.Meta()
		lmeta.control.command='exit'
		lmeta.recv_id=9
		lmeta.sender_id=9
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.node.ip, self.node.port))
		sock.send(lmeta.SerializePartialToString())
		sock.close()
		self.recieve_thread.join()



