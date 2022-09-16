import  json

data = {'0': '/Users/aqh/PycharmProjects/pythonProject/test/20200112112429   3   6-0.0.wav!左声道时域!2+/Users/aqh/PycharmProjects/pythonProject/test/20200112112429   3   6-0.0.wav!右声道时域!2+/Users/aqh/PycharmProjects/pythonProject/test/20200112112429   3   6-0.0.wav!左声道频域!2+/Users/aqh/PycharmProjects/pythonProject/test/20200112112429   3   6-0.0.wav!左声道频域!2+', '头': '波形处理0+2021-08-06 15:59:20 星期五+波形分析'}


with open("./logging.json",'r') as load_f:
    load_dict = json.load(load_f)



print(load_dict)


