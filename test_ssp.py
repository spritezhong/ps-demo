from schedule import ScheduleClass

from workandserver import PServerClass
from workandserver import server_handle

# from LRmodel import LRmodel
from LRssp import LRsspmodel

def main():
	master = ScheduleClass(3, 1, 3)
	master.start(0)
	server1 = PServerClass(0, '127.0.0.1', 8003, 'server', 0, 1)
	server_h1 = server_handle({0: 0.1, 1: 0.1, 2: 0.1})
	server1.set_reuqesthandle(server_h1.handle_request)
	server1.register()
	# lr=LRmodel(5)
	lr1=LRsspmodel(50,0,'127.0.0.1', 8005, 'worker', 0, 1)
	lr1.readdata('testSet.txt')
	lr1.train()
	lr1.stop()
	server1.stop()
	master.stop()


if __name__ == '__main__':main()
