import config
import logging
def get_serverkeyranges(num_servers):
	server_range=[]
	for i in range(num_servers):
		start=config.Max_Key/num_servers*i
		end=config.Max_Key/num_servers*(i+1)
		server_range.append([start,end])
	print('range: %d' %num_servers)
	print(server_range)

	return server_range

def getslicer(kv_list,range_list): #返回结果形式['flag',[key_list,val_list]]的
	num=len(range_list)
	pos=[0]*(num+1)
	begin=0
	cflag=[1]*(num+1)
	for i in range(num):
		# begin=
		if i==0:
			b_index=low_bound(kv_list[0][begin:],range_list[i][0])
			pos[0]=b_index
			begin+=b_index
		e_index=low_bound(kv_list[0][begin:],range_list[i][1])
		length=e_index-b_index
		begin=begin+length
		pos[i+1]=pos[i]+length
		if length==0:
			cflag[i]=0
	if pos[num]!=len(kv_list[0]):
		logging.error('slice failed')
	slicekv=[]
	for i in range(num):
		seg_keys=kv_list[0][pos[i]:pos[i+1]]
		if(len(kv_list)>1):
			seg_vals=kv_list[1][pos[i]:pos[i+1]]
		else:
			seg_vals=[0]*(pos[i+1]-pos[i])
		seg=[]
		seg.append(seg_keys)
		seg.append(seg_vals)
		slicekv.append([cflag[i],seg])
	return slicekv






def low_bound(array,val): #返回数组中第一个大于等于val索引
	low=0
	high=len(array)-1
	pos=len(array)
	while(low<high):
		mid=int((low+high)/2)
		if val>array[mid]:
			low=mid+1
		else:
			high=mid
			pos=high
	return pos


if __name__=='__main__':
	nums=[10,10,10,20,20,20,30,30]
	print(low_bound(nums,5))
	print(low_bound(nums, 10))
	print(low_bound(nums, 30))
	print(low_bound(nums, 35))
	range_list=[[0,10],[10,20],[20,30]]
	keys_list=[0,1,3,5,10,11,12,20,25]
	kv_list=[]
	kv_list.append(keys_list)
	pos=getslicer(kv_list,range_list)
	print(pos)
	a=pos[0]
	print(a[0])
	b=a[1]
	print(b[0])
	print(b[1])
