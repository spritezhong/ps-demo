from schedule import ScheduleClass
from workandserver import PWorkerClass
from workandserver import PServerClass
master=ScheduleClass(3,1,0)
master.start(0)
server1=PServerClass(0,'127.0.0.1',8003,'server',0,2,{0:0.1,1:0.1,2:0.1,3:0.1,4:0.1,5:0.1})
server1.register()
server2=PServerClass(1,'127.0.0.1',8004,'server',0,2,{6:0.2,7:0.1,8:0.1,9:0.6,10:0.1,11:0.1})
server2.register()

worker=PWorkerClass(2,'127.0.0.1',8001,'worker',0,2)
worker.register()
worker.waitready()
server1.waitready()
server2.waitready()
key_list=[i for i in range(12)]
b=[0]*12
worker.wait(worker.pull(key_list,b))
print('b',b)
worker.stop()
server1.stop()
server2.stop()
master.stop()
