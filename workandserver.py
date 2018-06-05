from single import SingleClass
import json
import message_pb2 as message
import allocate
import config
from single import CallBack
import logging
import csv



class PWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum):
		super(PWorkerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process,self.handle_clock)
		self.dict_callback={}         #<timestamp,callback>
		self.dict_kv={}       #存放每个timestamp的数据信息
		self.dict_arg={}     #每个dict_callback的参数

	def process(self,msg): #处理从服务器中pull下来的数据
		# print('process',json.loads(msg.body.decode()))
		if msg.push==False:
			ts=msg.timestamp
			self.mutex.acquire()
			if ts not in self.dict_kv.keys():
				self.dict_kv[ts]=[]
			self.dict_kv[ts].append(json.loads(msg.body.decode()))
			self.mutex.release()
			if self.tracker[ts][1]==self.servernum-1: #这里应该是等于服务器的数量-1因为当前回复的服务器未计算在内
				self.run_callback(ts)     #全部返回，执行回调函数
				self.printval()

	def add_callback(self,timestamp,callback):
		#这里需要互斥访问self.dict_callback，后期需要引入锁的机制
		self.mutex.acquire()
		self.dict_callback[timestamp]=callback
		self.mutex.release()

	def run_callback(self,timestamp):
		# print('run call back')
		self.mutex.acquire()
		if timestamp not in self.dict_callback.keys():
			return
		cb=self.dict_callback[timestamp]
		cb.run()
		del self.dict_callback[timestamp]     #从列表删除
		self.mutex.release()

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

	def update(self,*arg):
		ts=arg[0][2]
		results=self.dict_kv[ts]
		print('results',results)
		print('arg00',len(arg[0][0]),arg[0][0])
		len_key=0
		len_val=0
		for i in range(len(results)):
			len_key+=len(results[i][0])
			len_val+=len(results[i][1])

		if len(arg[0][0])!=len_key or len(arg[0][1])!=len_val:
			logging.error('lost some server response',arg[0][0],len_key,arg[0][1],len_val)

		sort_result=sorted(results)
		val_list=[]
		for i in range(len(sort_result)):
			val_list+=sort_result[i][1]
		for i in range(len(arg[0][1])):
			arg[0][1][i]=val_list[i]



	def pull(self,key_list,val_list):
		servernum =self.servernum #这里应该等于servergroup中的server数量
		kv_list=[]
		kv_list.append(key_list)
		kv_list.append(val_list)
		self.tracker.append([servernum, 0])
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
			print('skipnum',skipnum)
			self.tracker[ts][1]+=skipnum
		if skipnum==len(slicer):
			self.run_callback(ts)
		for i in range(len(slicer)):
			if slicer[i][0]=='False':
				continue
			msg=message.Meta()
			msg.sender_id=self.node.id
			msg.recv_id=config.serverranktoID(i)
			msg.body=json.dumps(slicer[i][1]).encode()
			msg.push=push
			msg.timestamp=ts
			msg.request=True
			self.send(msg)




	def printval(self):
		print('check weight',self.dict_kv)
		pass


	def wait(self,timestamp):
		while(self.tracker[timestamp][0]!=self.tracker[timestamp][1]):
			pass
			# print('wait')

class server_handle:
	def __init__(self,store):
		self.store=store
	def handle_request(self,msg,data,server):
		# print('data',data)
		# print('store',self.store)
		re_kvlist = []
		if msg.push==True:
			kv_list=data
			for i in range(len(kv_list[0])):
				index=kv_list[0][i]
				self.store[index]-=kv_list[1][i]
		else:
			re_vals=[]
			re_keys=[]

			kv_list=data
			for i in range(len(kv_list[0])):
				if int(kv_list[0][i]) not in self.store.keys():
					logging.error('cannot find key in server')
				re_keys.append(kv_list[0][i])
				re_vals.append(self.store[int(kv_list[0][i])])
			re_kvlist.append(re_keys)
			re_kvlist.append(re_vals)
		server.request_msg(msg,re_kvlist)


class PServerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum):
		super(PServerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process,self.handle_clock)
		# self.data=data     #存放参数值<key,value>形式
		# self.requesthandle=self.response

	def set_reuqesthandle(self,requesthandle):
		self.requesthandle=requesthandle
		# pass
	def process(self,msg):
		#本地复制下信息
		lmeta=message.Meta()
		lmeta.body=msg.body
		lmeta.timestamp=msg.timestamp
		lmeta.sender_id=msg.sender_id
		lmeta.recv_id=msg.recv_id
		lmeta.request=msg.request
		lmeta.push=msg.push
		self.requesthandle(lmeta,json.loads(lmeta.body.decode()),self)
		# cb= CallBack(self.requesthandle,lmeta)
		# cb.run()
		# self.response(lmeta)

	def savetodisk(self,data):
		with open(self.save_path,'w') as f:
			f_csv=csv.DictWriter(f,'feature_id')
			f_csv.writeheader()
			f_csv.writerows(data)

	def readfromdisk(self):
		with open(self.save_path,'r') as f:
			f_csv=csv.DictReader()
	def request_msg(self,request_msg,kvlist):
		lmeta = message.Meta()
		lmeta.sender_id = request_msg.recv_id
		lmeta.recv_id = request_msg.sender_id
		lmeta.timestamp = request_msg.timestamp
		lmeta.push = request_msg.push
		lmeta.body = json.dumps(kvlist).encode()
		lmeta.request = False
		self.send(lmeta)
'''
	def response(self,request_msg):
		lmeta=message.Meta()
		lmeta.sender_id=request_msg.recv_id
		lmeta.recv_id=request_msg.sender_id
		lmeta.timestamp=request_msg.timestamp
		lmeta.push=request_msg.push
		lmeta.body=request_msg.body
		lmeta.request=False
		if lmeta.push==True:
			kv_list=json.loads(lmeta.body.decode())
			for i in range(len(kv_list[0])):
				index=kv_list[0][i]
				self.data[index]-=kv_list[1][i]
		else:
			re_vals=[]
			re_keys=[]
			re_kvlist=[]
			kv_list = json.loads(lmeta.body.decode())
			for i in range(len(kv_list[0])):
				if int(kv_list[0][i]) not in self.data.keys():
					logging.error('cannot find key in server')
				re_keys.append(kv_list[0][i])
				re_vals.append(self.data[int(kv_list[0][i])])
			re_kvlist.append(re_keys)
			re_kvlist.append(re_vals)
			lmeta.body=json.dumps(re_kvlist).encode()
		# print('recv_id：%d' %lmeta.recv_id)
		self.send(lmeta) #根据request_msg中的节点id，查询节点相应的<ip,port>回复消息
'''

