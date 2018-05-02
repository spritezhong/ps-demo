import zmq
import logging
import message_pb2 as message
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
		addr="tcp://"+node.ip+":"+str(node.port)
		if(self.receiver.bind(addr)!=None):
			logging.error("bind port error")

	def connect(self,node,mynode):
		id=node.id
		if id in self.senders.keys():
			self.senders[id].close()
		if(node.role==mynode.role and node.id!=mynode.id):
			return
		sender=self.context.socket(zmq.DEALER)
		# if mynode.id!=-1:
		# 	sender.setsockopt(zmq.IDENTITY,str(mynode.id).encode())
		addr= "tcp://" + node.ip + ":" + str(node.port)
		# print('my node connect addr',mynode.role,mynode.id,addr)
		if sender.connect(addr)!=None:
			logging.error("connect node error")
		self.senders[id]=sender

	def sendmsg(self,msg):
		id=int(msg.recv_id)
		if id not in self.senders.keys():
			logging.error('cannot find sender')
			# print('revv id is:',id)
		sock=self.senders[id]
		# print('recv id is :',str(id))
		# sock.send_multipart([str(id).encode(), msg.SerializePartialToString()])
		sock.send(msg.SerializePartialToString())
		# print('sender',msg.SerializePartialToString())

	def recvmsg(self):
		# print('zmqsock recvmsg')
		for i in range(1):
			self.receiver.recv()
		buf= message.Meta()

		# print('recvmsg',self.receiver.recv())
		buf.ParseFromString(self.receiver.recv())
		# print("receive messge is",buf)
		return buf









