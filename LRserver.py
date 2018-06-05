# class LRserver:
# 	def __init__(self,store):
# 		self.store=store
# 	def handle_request(self,msg,data,server):


'''
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
'''