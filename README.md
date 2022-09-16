# sona
sona detection

### 预处理
预处理主要把pcm等格式音频处理成常用wav格式，放在predata.py里，analysisdata.py用于分析数据。

### 降噪
降噪代码分为经典降噪和模型降噪两部分

经典降噪：karman.py，ffl.py，wavereduce.py

模型降噪：采用的wavenet网络，模型参数太大，没上传，建议改小网络结构重新训练

### 分类
分类模块用的gbdt2nn网络，效果不好。

另外分类方式不符合要求，应该是二分类结构，建议换模型。

###程序运行
sona2是最新的版本，sona1是之前版本
```
python sona2.py
```

###环境
由于我没有单独为这个项目创建环境，所有依赖都放在里面，可以看情况安装