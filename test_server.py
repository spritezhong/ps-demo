#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import socket
import google.protobuf
import  addressbook_pb2
import json

address=('127.0.0.1',8001)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(address)
sock.listen(5)
list_conn=[]
addr_info=addressbook_pb2.Person()
while True:
    conn,addr=sock.accept()
    list_conn.append(conn)
    info=conn.recv(2048).decode()
    print(json.loads(info))
    # addr_info.ParseFromString(info)
    # infoss= json.loads(info)
    # print(addr_info)
    break
    # print(type(infoss)=='list')
    # addr_info.ParseFromString(info)
    # print(addr_info.type)
for i in list_conn:
    i.send(('please go out!').encode())
    i.close()
# sock.close()
#解析从客户端发来的指令，如果指令为'pull'发送参数给服务器端,否则执行函数update

'''
if __name__=='__main__':
    import socket
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('localhost',8001))
    sock.listen(5)
    while True:
        connection,address=sock.accept()
        try:
            connection.settimeout(5)
            buf=connection.recv(1024).decode()
            if buf=='1':
                connection.send(('welcome to server!').encode())
            else:
                connection.send(('please go out!').encode())
        except socket.timeout:
            print('time out')
        connection.close()
'''

