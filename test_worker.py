#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import socket
import json
import addressbook_pb2 as addressbook
person = addressbook.Person()
# blob=addressbook.Blob()
# for i in range(4):
#     list_idx=blob.feature_index.add_id(i)
# print(list_idx.size())
#
# blob.type='pull'
# blob.feature_val=[0.2,0.1,0.3,0.1]
person.id = 1234
# person.name = "John Doe"
person.email = "jdoe@example.com"
# phone = person.phones.add() #phones字段是符合类型，调用add()方法初始化新实例。如果phones字段是标量类型，直接append()添加新元素即可。
# phone.number = "555-4321"
# phone.type = addressbook.Person.HOME
id=[1,2,3,4,5]
vec=[]
vec.append(id)
val=[0.1,0.1,0.1,0.1,0.1]
vec.append(val)
print(len(vec))
# vectype=[type(id)]
# print(len(vectype))
# dict={}
# dict[type(id)]=vec[0]
# print(dict)

address=('127.0.0.1',8001)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(address)
mylist=[1,2,3,4,5]
dict1={'a':1,'b':2}
vec=1
json_string=json.dumps(vec)
sock.send(json_string.encode())

# json_string=json.dumps(person)
# info=json.loads(json_string)
# sock.send(person.SerializePartialToString())
ss=sock.recv(2048).decode()
print(ss)
# sock.send(blob.SerializePartialToString())
sock.close()


