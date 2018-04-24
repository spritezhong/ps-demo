Max_Key=10 #一个server上最多能运行的key


def workranktoID(self, rank):
	return rank * 2 + 9


def serverranktoID(self, rank):
	return rank * 2 + 8


def IDtorank(self, id):
	return max((id - 8) / 2, 0)