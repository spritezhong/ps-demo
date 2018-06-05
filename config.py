Max_Key=12 #一个server上最多能运行的key 配置文件


def workranktoID(rank):
	return rank * 2 + 9


def serverranktoID(rank):
	return rank * 2 + 8


def IDtorank(id):
	return max((id - 8) / 2, 0)
