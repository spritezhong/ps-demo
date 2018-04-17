from schedule import ScheduleClass
from single import PWorkerClass
from single import PServerClass
def Handle():
	print("send success")
master=ScheduleClass(2,1)
master.start(0)
server=PServerClass(1,'localhost',8003,'worker',0,{0:0.1,1:0.1,2:0.1})
server.register()
worker=PWorkerClass(2,'localhost',8001,'worker',0)
worker.register()
worker.pull({0:0,1:0,2:0})
worker.printval()
# single.stop()
# master.stop()