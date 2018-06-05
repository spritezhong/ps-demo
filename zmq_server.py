import zmq
import time
import message_pb2 as mess
context=zmq.Context()
# socket=context.socket(zmq.REP)
socket=context.socket(zmq.ROUTER)
print(socket==None)

print(socket.bind("tcp://127.0.0.1:8888"))
# print(socket.bind("tcp://*:8888"))
while True:
	for i in range(1):
		message = socket.recv()
	msg=mess.Meta()
	msg.recv_id=5
	message=socket.recv()
	print("Received request:",message)
	time.sleep(1)
	# ident = random.choice([b'A', b'A', b'B'])
	# And then the workload
	work = b"This is the workload"
	socket.send_multipart([b'A', msg.SerializePartialToString()])
	# socket.send(msg.SerializePartialToString())
