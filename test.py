# import addressbook_pb2 as addressbook
#
# person = addressbook.Person()
# person.id = 1234
# person.name = "John Doe"
# person.email = "jdoe@example.com"
# phone = person.phones.add() #phones字段是符合类型，调用add()方法初始化新实例。如果phones字段是标量类型，直接append()添加新元素即可。
# phone.number = "555-4321"
# phone.type = addressbook.Person.HOME
# print(person)
import random
import numpy as np
# dict_w={}
# list1=[1,2,4,5]
# for i in list1:
#     dict_w[i]=random.random()
# print(dict_w)
# v=[]
# for i in range(5):
#     v.append([i])
# print(v)
# av=np.array(v)
# print(av)
# for i in range(5):
#     print(av[i,0])

class CallBack:
    def __init__(self,fun,*arg):
        self.arg=arg
        self.fun=fun

    def run(self):
        self.fun(self.arg)
def fun(*num):
    print(num[0][1])
    a=[2,3,4]
    num[0][1]=a
    # for i in range(len(num[0][1])):
    #     num[0][1][i]=i
    # print(num[0][0])
    # for i in num:
    #     print(i)
   # print('num1 is:%d num2 is:%d' %num1,num2)

def ff(*num):
    a=num[0][0]
    print(type(num[0][0]))
    # num[0][0]=a+1
    # num[0][0]=num[0][0]+1
    # print(num[0][0])
def addcallback(ts,cb):
    back=[]
    back.append(cb)
    return back
# a=[0,0,0]
# b=[0,1,2]
# cb=CallBack(fun,b,a)
# bb=addcallback(0,cb)
# bb[0].run()
# print(a)
mm=ff
class f2:
    def __init__(self, data):
        self.data=data
    def cc(self,num):
        self.data+=num
        print('data:',self.data)

def set_fun(f):
    mm=f
fa=f2(0)
mm=fa.cc
mm(1)
mm(2)
# cb=CallBack(mm,1,2)
# cb.run()
'''
import message_pb2 as mess
import json
node=mess.Node()
nodelist=mess.NodeList()
node.id=1
node.ip='127.0.0.1'
node.port=8005
node1=mess.Node()
node1.id=1
node1.ip='127.0.0.1'
node1.port=8005
newnode=nodelist.nodel.add()
newnode.id=node.id
newnode.ip=node.ip
# print(newnode)
# print('nodelist',nodelist)
newnode=nodelist.nodel.add()
newnode.id=node1.id
# nodelist.append(node)
# nodelist.append(node1)
# nodelist[0]=node.SerializePartialToString()
msg=mess.Meta()
msg.body=nodelist.SerializePartialToString()
# print(msg.body)
nodelist1=mess.NodeList()
nodelist1.ParseFromString(msg.body)
print(nodelist1.nodel[0])
for i in nodelist1.nodel:
    print(i.id)

import csv
def savetodisk(data):
    with open(r"f:\DL\test.csv", 'w') as f:
        f_csv = csv.DictWriter(f)
        f_csv.writeheader()
        f_csv.writerows(data)


def readfromdisk():
    with open('f\DL\test.csv', 'r') as f:
        f_csv = csv.DictReader()
# print(msg.body)
# strs=(msg.body.decode())
# print(len(strs.split(',')))
# print(list(strs))

data={0:0.1,1:0.1,2:0.1,3:0.1,4:0.1,5:0.1}
savetodisk(data)
'''