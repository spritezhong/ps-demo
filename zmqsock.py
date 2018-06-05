import zmq
import logging
import message_pb2 as message
#class ZMQSOCK 采用dealer+router通信机制，封装bind,connect,send,recv方法
class ZMQSOCK:
	def __init__(self):
		self.senders={}
		self.context=None
		self.receiver=None
	'''
	start方法用来创建包含I/O线程的context
	'''
	def start(self):
		if(self.context==None):
			self.context=zmq.Context()
	'''
	stop关闭self.reciever和self.senders
	'''
	def stop(self):
		logging.info("is stopping")
		self.receiver.close()
		for key in self.senders.keys():
			self.senders[key].close()

	'''
	bind 绑定相应的端口
	@param node 绑定节点node的ip和ort
	'''
	def bind(self,node):
		self.receiver=self.context.socket(zmq.ROUTER)
		addr="tcp://"+node.ip+":"+str(node.port)
		if(self.receiver.bind(addr)!=None):
			logging.error("bind port error")
	'''
	connect 连接到某ip
	@param node,mynode  意味着mynode节点连接上node节点
	'''
	def connect(self,node,mynode):
		id=node.id
		if id in self.senders.keys():
			self.senders[id].close()
		if(node.role==mynode.role and node.id!=mynode.id):
			return
		sender=self.context.socket(zmq.DEALER)
		addr= "tcp://" + node.ip + ":" + str(node.port)
		if sender.connect(addr)!=None:
			logging.error("connect node error")
		self.senders[id]=sender
	'''
    sendmsg 发送消息
    @parama msg 待发送的消息，是message结构
	'''
	def sendmsg(self,msg):
		id=int(msg.recv_id)
		if id not in self.senders.keys():
			logging.error('cannot find sender')
		sock=self.senders[id]
		sock.send(msg.SerializePartialToString())
	'''
	recvmsg 接收消息
	@return buf 返回消息接收到的buf,buf也是message结构
	'''
	def recvmsg(self):
		for i in range(1):
			self.receiver.recv()
		buf= message.Meta()
		buf.ParseFromString(self.receiver.recv())
		return buf









