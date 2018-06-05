import allocate
import config
from single import CallBack
from single import SingleClass
import logging
import json
import message_pb2 as message


class SSPWorkerClass(SingleClass):
	def __init__(self,id,ip,port,role,client_id,servernum):
		super(SSPWorkerClass, self).__init__(id,ip,port,role,client_id,servernum,self.process,self.handle_clock)
		self.dict_callback={}         #<timestamp,callback>
		self.dict_kv={}       #存放每个timestamp的数据信息
		self.dict_arg={}     #每个dict_callback的参数
		self.min_clock=0         #用于ssp的时间机制
		# self.staleness=staleness
		self.dict_clock={}  #存放每个worker的clock
		self.flag_clock=False

	def process(self,msg): #处理从服务器中pull下来的数据
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
		# print('update')
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

	def pullarg(self,*arg):
		key_list=arg[0][0]
		val_list=arg[0][1]
		# print('pull')
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




	def sendclock(self,clock,ts):
		msg = message.Meta()
		schedule_node = message.Node()
		schedule_node.id = 1
		schedule_node.ip = '127.0.0.1'
		schedule_node.port = 8002
		msg.control.command = 'ssp'
		msg.control.reg_node.ip = self.node.ip
		msg.control.reg_node.port = self.node.port
		msg.control.reg_node.role = self.node.role
		msg.timestamp =ts
		msg.sender_id=self.node.id
		msg.recv_id = schedule_node.id
		msg.body=str(clock).encode()
		self.zmqs.sendmsg(msg)
	def pullwithclock(self,key_list,val_list,stale):
		self.flag_clock=False
		self.tracker.append([1, 0])
		ts=len(self.tracker)-1
		cb=CallBack(self.pullarg,key_list,val_list)
		self.add_callback(ts,cb)
		self.sendclock(stale,ts)
		return ts



	def handle_clock(self,msg):
		# print('handle clock ssp',msg.body.decode())
		ts = msg.timestamp
		self.mutex.acquire()
		cbs = self.dict_callback[ts]
		del self.dict_callback[ts]  # 从列表删除
		self.mutex.release()
		if msg.body.decode()=='True':
			# print('comminy')
			self.flag_clock=True

			cbs.run()
		else:
			self.flag_clock=False


	def sendkv(self,ts,push,kv_list):
		slicer=allocate.getslicer(kv_list,allocate.get_serverkeyranges(self.servernum))  #根据serverrange查询每个server负责的key
		skipnum=0
		# print('len slice is:%d'% len(slicer))
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
			msg.recv_id=config.serverranktoID(i)
			msg.body=json.dumps(slicer[i][1]).encode()
			msg.push=push
			msg.timestamp=ts
			msg.request=True
			self.send(msg)




	def printval(self):
		pass


	def wait(self,timestamp):
		while(self.tracker[timestamp][0]!=self.tracker[timestamp][1]):
			pass
		return self.flag_clock
