from single import SingleClass
import json
import message_pb2 as message
import allocate
import config
from single import CallBack
import logging
class PWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum):
		super(PWorkerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process)
		self.dict_callback={}         #<timestamp,callback>
		self.dict_kv={}       #存放每个timestamp的数据信息
		self.dict_arg={}     #每个dict_callback的参数
	def process(self,msg): #处理从服务器中pull下来的数据
		if msg.push==False:
			ts=msg.timestamp
			if ts not in self.dict_kv.keys():
				self.dict_kv[ts]=[]
			self.dict_kv[ts].append(json.loads(msg.body.decode()))
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
	# def add_callarg(self,timestamp,*arg):  #现在回调函数和参数是分开存的，咋存一起呢？
	# 	self.dict_arg[timestamp]=arg

	def run_callback(self,timestamp):
		# print('run call back')
		if timestamp not in self.dict_callback.keys():
			return
		cb=self.dict_callback[timestamp]
		cb.run()
		#这里应该保证操作互斥，后期加锁
		# if timestamp not in self.dict_arg.keys():
		# 	self.dict_callback[timestamp]
		# else:
		# 	self.dict_callback[timestamp](self.dict_arg[timestamp][0],self.dict_arg[timestamp][1])         #执行回调函数
		# 	del self.dict_arg[timestamp]
		# print("已经执行回调函数")
		del self.dict_callback[timestamp]     #从列表删除

	def push(self,key_list,val_list,callback):
		server_num=self.servernum
		self.tracker.append([server_num,0])
		ts=len(self.tracker)-1
		self.add_callback(ts,callback)
		kv_list=[]
		kv_list.append(key_list)
		kv_list.append(val_list)
		self.sendkv(ts,True,kv_list)
		return ts
	'''
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
	'''
	def update(self,*arg):
		ts=arg[0][2]
		results=self.dict_kv[ts]
		len_key=0
		len_val=0
		for i in range(len(results)):
			len_key+=len(results[i][0])
			len_val+=len(results[i][1])
		if len(arg[0][0])!=len_key or len(arg[0][1])!=len_val:
			logging.error('lost some server response')

		sort_result=sorted(results)
		val_list=[]
		for i in range(len(sort_result)):
			val_list+=sort_result[i][1]
		for i in range(len(arg[0][1])):
			arg[0][1][i]=val_list[i]

	# def update(self,data,ts):
	# 	# print('回调updata')
	# 	self.dict_kv[ts]=data
	# 	# data=self.dict_kv[ts]
	# 	# print(data)
	'''
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
		# print('pull')
		self.send(msg)  # 需要根据参数的id，查找对应server的id，发送消息

		return ts
	'''

	def pull(self,key_list,val_list):
		self.servernum =self.servernum #这里应该等于servergroup中的server数量
		kv_list=[]
		kv_list.append(key_list)
		kv_list.append(val_list)
		self.tracker.append([self.servernum, 0])
		ts=len(self.tracker)-1
		cb=CallBack(self.update,key_list,val_list,ts)
		self.add_callback(ts,cb)
		# self.add_callback(ts,self.update)
		# self.add_callarg(ts,key_list,val_list)
		self.sendkv(ts,False,kv_list)

		return ts



	def sendkv(self,ts,push,kv_list):
		slicer=allocate.getslicer(kv_list,allocate.get_serverkeyranges(self.servernum))  #根据serverrange查询每个server负责的key
		skipnum=0
		print('len slice is:%d'% len(slicer))
		for i in range(len(slicer)):
			if slicer[i][0]=='False':
				skipnum=skipnum+1
			self.tracker[ts][1]+=skipnum
		if skipnum==len(slicer):
			self.run_callback(ts)
		for i in range(len(slicer)):
			if slicer[i][0]=='False':
				continue
			msg=message.Meta()
			msg.sender_id=self.node.id
			print('send_id :%d' %msg.sender_id)
			msg.recv_id=config.serverranktoID(i)
			msg.body=json.dumps(slicer[i][1]).encode()
			msg.push=push
			msg.timestamp=ts
			msg.request=True
			self.send(msg)




	def printval(self):
		print('check weight')
		print(self.dict_kv)


	def wait(self,timestamp):
		while(self.tracker[timestamp][0]!=self.tracker[timestamp][1]):
			pass
			# print('wait')


class PServerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum,data):
		super(PServerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process)
		self.data=data     #存放参数值<key,value>形式
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
		# kv_list=json.loads(lmeta.body.decode())
		# print('dict_data',dict_data)
		# print(dict_data)
		if lmeta.push==True:
			kv_list=json.loads(lmeta.body.decode())
			for i in range(len(kv_list[0])):
				index=kv_list[0][i]
				self.data[index]-=kv_list[1][i]
			# grad = json.loads(lmeta.body.decode())  # 后续需要改进
			# for id in dict_data.keys():
			# 	if id in self.data.keys():
			# 		self.data[id] -= dict_data[id]
		else:
			re_vals=[]
			re_keys=[]
			re_kvlist=[]
			kv_list = json.loads(lmeta.body.decode())
			print('kvlist:%s'%kv_list)
			for i in range(len(kv_list[0])):
				if int(kv_list[0][i]) not in self.data.keys():
					logging.error('cannot find key in server')
				re_keys.append(kv_list[0][i])
				re_vals.append(self.data[int(kv_list[0][i])])
			re_kvlist.append(re_keys)
			re_kvlist.append(re_vals)
			lmeta.body=json.dumps(re_kvlist).encode()
		print('recv_id：%d' %lmeta.recv_id)
		self.send(lmeta) #根据request_msg中的节点id，查询节点相应的<ip,port>回复消息

