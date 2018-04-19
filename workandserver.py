from single import SingleClass
import json
import message_pb2 as message
class PWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum):
		super(PWorkerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process)
		self.dict_callback={}         #<timestamp,callback>
		self.dict_kv={}       #存放每个timestamp的数据信息
		self.dict_arg={}     #每个dict_callback的参数
	def process(self,msg): #处理从服务器中pull下来的数据
		if msg.push==False:
			ts=msg.timestamp
			self.dict_kv[ts]=json.loads(msg.body.decode())
			# print('worker process timestamp:%d'%ts)
			# print(self.tracker[ts][1])
			# print('dict-kv')
			# print(self.dict_kv[ts])
			if self.tracker[ts][1]==self.servernum-1: #这里应该是等于服务器的数量-1因为当前回复的服务器未计算在内
				self.run_callback(ts)     #全部返回，执行回调函数
			self.printval()

	def add_callback(self,timestamp,callback):
		#这里需要互斥访问self.dict_callback，后期需要引入锁的机制
		self.dict_callback[timestamp]=callback
	def add_callarg(self,timestamp,*arg):  #现在回调函数和参数是分开存的，咋存一起呢？
		self.dict_arg[timestamp]=arg

	def run_callback(self,timestamp):
		# print('run call back')
		if timestamp not in self.dict_callback.keys():
			return
		#这里应该保证操作互斥，后期加锁
		if timestamp not in self.dict_arg.keys():
			self.dict_callback[timestamp]
		else:
			self.dict_callback[timestamp](self.dict_arg[timestamp][0],self.dict_arg[timestamp][1])         #执行回调函数
			del self.dict_arg[timestamp]
		# print("已经执行回调函数")
		del self.dict_callback[timestamp]     #从列表删除

	def push(self,dict_grad,callback): #callback是消息被服务器接受后执行的函数
		server_num=1 #getnum(ServerGroup)与之通信的服务器组内的服务器数量

		#需要进一步完善。。。。。。。。。。。。。
		msg = message.Meta()
		msg.body=json.dumps(dict_grad).encode()

		msg.request=True
		msg.push=True
		msg.sender_id=self.node.id
		self.tracker.append([server_num,0])
		ts=len(self.tracker) - 1
		msg.timestamp = ts
		self.add_callback(msg.timestamp,callback)
		# self.send(ip, port, msg)
		msg.recv_id=8#暂不考虑根据key值，查找对应机器的id
		self.send(msg) #需要根据参数的id，查找对应server的id，发送消息
		return ts
	def update(self,data,ts):
		# print('回调updata')
		data=self.dict_kv[ts]
		# print(data)
	def pull(self,dict_w):
		self.servernum = 1
		msg = message.Meta()
		msg.body = json.dumps(dict_w).encode()
		self.tracker.append([self.servernum, 0])
		ts=len(self.tracker)-1
		msg.timestamp =ts
		msg.request = True
		msg.push=False
		msg.sender_id = self.node.id
		msg.recv_id =8  # 暂不考虑根据key值，查找对应机器的id

		self.add_callback(msg.timestamp,self.update)
		self.add_callarg(msg.timestamp,dict_w,msg.timestamp)
		#增加回调函数，一旦获得服务器回复，更新dict_w
		self.send(msg)  # 需要根据参数的id，查找对应server的id，发送消息
		return ts

	def printval(self):
		print('check weight')
		print(self.dict_kv)


	def wait(self,timestamp):
		while(self.tracker[timestamp][0]!=self.tracker[timestamp][1]):
			print('wait')


class PServerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum,data):
		super(PServerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process)
		self.data=data     #存放参数值
		# self.handle=handle

	def process(self,msg):
		#本地复制下信息
		lmeta=message.Meta()
		lmeta.body=msg.body
		lmeta.timestamp=msg.timestamp
		lmeta.sender_id=msg.sender_id
		lmeta.recv_id=msg.recv_id
		lmeta.request=msg.request
		lmeta.push=msg.push
		self.response(lmeta)
		#这里应该等待含有改段参数梯度值的worker全部发送数据过来
		# if lmeta.request==False:     #表示传来的是push请求
		# 	grad =json.loads(lmeta.body.decode())  # 后续需要改进
		# 	for id in grad.keys():
		# 		if id in self.data.keys():
		# 			self.data[id] -= grad[id]
		# else:
		# 	self.response(lmeta)


		##########################


	def response(self,request_msg):
		lmeta=message.Meta()
		lmeta.sender_id=request_msg.recv_id
		lmeta.recv_id=request_msg.sender_id
		lmeta.timestamp=request_msg.timestamp
		lmeta.push=request_msg.push
		lmeta.body=request_msg.body
		lmeta.request=False
		dict_data=json.loads(lmeta.body.decode())
		# print('dict_data',dict_data)
		# print(dict_data)
		if lmeta.push==True:
			# grad = json.loads(lmeta.body.decode())  # 后续需要改进
			for id in dict_data.keys():
				if id in self.data.keys():
					self.data[id] -= dict_data[id]
		else:
			re_vals={}
			for key in dict_data.keys():
				if int(key) in self.data.keys():
					# print('===')
					re_vals[key]=self.data[int(key)]
			lmeta.body=json.dumps(re_vals).encode()
			# print('send pull')
			# print(json.loads(lmeta.body.decode()))
		#################待完善#############
		#需要添加一个根据节点id查询节点<ip,port>的函数
		self.send(lmeta) #根据request_msg中的节点id，查询节点相应的<ip,port>回复消息

