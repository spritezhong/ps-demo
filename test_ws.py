from schedule import ScheduleClass
from single import PWorkerClass
from single import PServerClass
def Handle():
	print("send success")
master=ScheduleClass(2,1)
master.start(0)
server=PServerClass(8,'localhost',8003,'server',0,1,{0:0.1,1:0.1,2:0.1})
server.register()
worker=PWorkerClass(9,'localhost',8001,'worker',0,1)
worker.register()
worker.wait(worker.pull({0:0,1:0,2:0}))
# worker.printval()
# single.stop()
# master.stop()