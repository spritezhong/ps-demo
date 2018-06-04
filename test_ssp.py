from schedule import ScheduleClass
from workandserver import PWorkerClass
from workandserver import PServerClass



key_list=[i for i in range(12)]
worker.wait(worker.pull(key_list,[0]*12))
worker.stop()
server1.stop()
server2.stop()
master.stop()

def main():
	master = ScheduleClass(3, 1, 0)
	master.start(0)
	server1 = PServerClass(0, '127.0.0.1', 8003, 'server', 0, 2, {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1})
	server1.register()
	server2 = PServerClass(1, '127.0.0.1', 8004, 'server', 0, 2, {6: 0.2, 7: 0.1, 8: 0.1, 9: 0.6, 10: 0.1, 11: 0.1})
	server2.register()
	worker = PWorkerClass(2, '127.0.0.1', 8001, 'worker', 0, 2)
	worker.register()
	worker.waitready()
	server1.waitready()
	server2.waitready()

    work.read_data('testSet.txt')
    # serv.process() 后面需要更改开多个进程，一个进程运行服务器，另一个进程跑主程序
	#
    # print('sddddddd')
    for i in range(10): #在运行这段程序之前要保证服务器已经开始运转
        work.pull()
        work.calc_gradient()
        work.push()

    work.pull()
    work.predict()
    print('test over!')
    #

if __name__ == '__main__':main()
