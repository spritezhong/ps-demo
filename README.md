# ps-demo
支持多个server和多个worker通信
workerandserver中对应的是不含ssp功能版本，而sspwork支持ssp功能。
以testset数据集为例，先运行test_ssp（1个schedule,1serverr,1个worker启动），在运行test_ssp_w2（另启动一个worker）可测试ssp功能。 
