from schedule import ScheduleClass
from single import SingleClass
def Handle():
	print("send success")
master=ScheduleClass(1,1)
master.start(0)
single=SingleClass(2,'localhost',8001,'worker',0,Handle)
single.register()
single.stop()
# master.stop()