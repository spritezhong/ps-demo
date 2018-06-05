from LRssp import LRsspmodel
lr2=LRsspmodel(50,1,'127.0.0.1', 8006, 'worker', 1, 1)
lr2.readdata('testSet.txt')
lr2.train()
lr2.stop()
