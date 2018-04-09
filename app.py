from server import ServerClass
from worker import WorkerClass





def main():
    work=WorkerClass([0,1,2])
    # serv=ServerClass(0.1,[0,1,2])
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





