import zmq
import logging
class ZMQSOCK:
	def __init__(self):
		self.senders={}
		self.context=None
		self.receiver=None
	def start(self):
		if(self.context==None):
			self.context=zmq.Context()

	def bind(self,node):
		self.receiver=self.context.socket(zmq.ROUTER)
		# ip=node.ip
		addr="tcp://"+node.ip+":"+node.port
		if(self.receiver.bind(addr)!=None):
			logging.error("bind port error")

	def connect(self,node,mynode):
		id=node.id
		if id in self.senders.keys():
			self.senders[id].close()
		if(node.role==mynode.role and node.id!=mynode.id):
			return
		sender=self.context.socket(zmq.DEALER)
		sender.setsockopt(zmq.IDENTITY,mynode.id,len(mynode.id))
		addr= "tcp://" + node.ip + ":" + node.port
		if sender.connect(addr)!=None:
			logging.error("connect node error")
		self.senders[id]=sender

	def sendmsg(self,msg):
		id=int(msg.recv_id)
		if id not in self.senders.keys():
			logging.error('cannot find sender')
			print('sender id is:',id)
		sock=self.senders[id]
		sock.send_string(msg)

	def recvmsg(self):
		msg=self.receiver.recv()
		print("receive messge is",msg)
		return msg









