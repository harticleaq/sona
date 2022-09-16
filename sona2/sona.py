import json
import os
import time

import PyQt5.QtWidgets
import  matplotlib.pyplot as plt
from PyQt5 import QtCore,QtWidgets,QtGui,Qt
import sys
import predata
import analysisdata
from numpy import log10
import numpy as np
import ffl
import gc
import batch_sample
from wavereduce import wavereduce
from karman import karmanfilter
from create_mixed_audio_file import addNoise
import sonaModel
import images

class SonaWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SonaWindow,self).__init__()
        self.initUI()
        self.url = ''
        self.wavelist = []
        self.samplenum = ''
        self.waveaisle = ''
        self.savepath = './'
        self.wavfile = ''
        self.noisefile = ''


    def initUI(self):
        self.setWindowTitle('Sona波形处理')
        self.resize(1000,650)

        # self.setWindowOpacity(0.97)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setStyleSheet('background:white;')

        self.mainLayout = QtWidgets.QGridLayout()
        self.leftWidget = QtWidgets.QWidget()
        self.leftLayout = QtWidgets.QGridLayout()
        self.leftWidget.setLayout(self.leftLayout)
        self.rightWidget = QtWidgets.QStackedWidget()


        self.mainLayout.addWidget(self.leftWidget,0,0,8,2)
        self.mainLayout.addWidget(self.rightWidget,0,2,8,12)
        self.setLayout(self.mainLayout)

        self.label1 = QtWidgets.QPushButton('文件')
        self.label2 = QtWidgets.QPushButton('音频')
        self.label3 = QtWidgets.QPushButton('已完成')
        self.label1.setObjectName('left_label')
        self.label2.setObjectName('left_label')
        self.label3.setObjectName('left_label')

        self.btn1 = QtWidgets.QPushButton('首页')
        self.btn2 = QtWidgets.QPushButton('文件转换')
        self.btn3 = QtWidgets.QPushButton('波形分析')
        self.btn4 = QtWidgets.QPushButton('降噪处理')
        self.btn5 = QtWidgets.QPushButton('已存数据')
        self.btn6 = QtWidgets.QPushButton('模型降噪')

        self.btn6.setObjectName('left_button')
        self.btn6.setProperty('name','6')
        self.btn1.setObjectName('left_button')
        self.btn1.setProperty('name','1')
        self.btn2.setProperty('name','2')
        self.btn3.setProperty('name','3')
        self.btn4.setProperty('name','4')
        self.btn5.setProperty('name','5')

        self.btn2.setObjectName('left_button')
        self.btn3.setObjectName('left_button')
        self.btn4.setObjectName('left_button')
        self.btn5.setObjectName('left_button')
        self.btn1.setIcon(QtGui.QIcon(':/icons/首页.png'))
        self.btn2.setIcon(QtGui.QIcon(':/icons/转换 (2).png'))
        self.btn3.setIcon(QtGui.QIcon(':/icons/波形图 (1).png'))
        self.btn4.setIcon(QtGui.QIcon(':/icons/波形图.png'))
        self.btn5.setIcon(QtGui.QIcon(':/icons/保存.png'))
        self.btn6.setIcon(QtGui.QIcon('./icons/模型中心.png'))

        self.leftLayout.addWidget(self.label1)
        self.leftLayout.addWidget(self.btn1)

        self.leftLayout.addWidget(self.btn2)
        self.leftLayout.addWidget(self.label2)
        self.leftLayout.addWidget(self.btn3)
        self.leftLayout.addWidget(self.btn4)
        self.leftLayout.addWidget(self.label3)
        self.leftLayout.addWidget(self.btn5)
        self.leftLayout.addWidget(self.btn6)
        self.btn_pad = QtWidgets.QPushButton()
        self.leftLayout.addWidget(self.btn_pad)
        self.btn_pad2 = QtWidgets.QPushButton()
        self.leftLayout.addWidget(self.btn_pad2)
        self.btn_pad3 = QtWidgets.QPushButton()
        self.leftLayout.addWidget(self.btn_pad3)

        self.setObjectName('window')
        self.setStyleSheet('#window{background:#1D1F21;}')





        self.leftWidget.setStyleSheet('''
            
        QPushButton{border:none;font-size:16px;color:white;}  
        QPushButton#left_button:hover{ color:#C72426;border-bottom:4px solid rgba(255,255,255,0);
        font-weight:700;text-align: center
        }
        
        QPushButton#left_label{
            color:#D0A363;
            padding-bottom:5px;
            border-bottom:2px solid #DADADA;
            font-size:17px;
            font-weight:900;
            font-family: Helvetica Neue,Tahoma;
        }

        ''')



        self.btn1.clicked.connect(self.select_Widget)
        self.btn2.clicked.connect(self.select_Widget)
        self.btn3.clicked.connect(self.select_Widget)
        self.btn4.clicked.connect(self.select_Widget)
        self.btn5.clicked.connect(self.select_Widget)
        self.btn6.clicked.connect(self.select_Widget)

        self.rightWidget0 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget0)
        self.rightWidget1 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget1)
        self.rightWidget2 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget2)
        self.rightWidget3 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget3)
        self.rightWidget4 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget4)
        self.rightWidget5 = QtWidgets.QTableWidget()
        self.rightWidget.addWidget(self.rightWidget5)
        self.rightWidget6 = QtWidgets.QWidget()
        self.rightWidget.addWidget(self.rightWidget6)


        self.rightWidget1.setObjectName('rightWidget1')
        self.rightWidget2.setObjectName('rightWidget2')
        self.rightWidget3.setObjectName('rightWidget3')
        self.rightWidget4.setObjectName('rightWidget4')
        self.rightWidget5.setObjectName('rightWidget5')
        self.rightWidget6.setObjectName('rightWidget6')

        self.rightWidget1_layout=QtWidgets.QGridLayout()
        self.rightWidget0.setObjectName('rightWidget0')
        self.rightWidget1.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget2.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget3.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget4.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget5.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget6.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rightWidget1.setLayout(self.rightWidget1_layout)
        self.rightWidget1_layout.setContentsMargins(0, 0, 0, 0)


        self.rightWidget.setCurrentIndex(1)
        #窗口1布局
        # self.rightWidget1_logo= QtWidgets.QWidget()
        # self.rightWidget1_layout.addWidget(self.rightWidget1_logo,0,0,1,1)


        self.rightWidget1_up = QtWidgets.QWidget()
        self.rightWidget1_down = QtWidgets.QWidget()
        self.rightWidget1_layout.addWidget(self.rightWidget1_down,4,0,8,7)
        self.rightWidget1_layout.addWidget(self.rightWidget1_up,0,0,6,7)

        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(QtGui.QPixmap('./Sona处理.png'))
        self.rightWidget1_layout.addWidget(self.logo,0,0,1,1)
        self.logo.setContentsMargins(10,10,-1,-1)


        self.rightWidget1_up_layout = QtWidgets.QHBoxLayout()
        self.rightWidget1_up.setLayout(self.rightWidget1_up_layout)
        self.rightWidget1_up.setObjectName('rightWidget1_up')
        self.rightWidget1_down.setObjectName('rightWidget1_down')
        self.rightWidget1_down_layout = QtWidgets.QHBoxLayout()
        self.rightWidget1_down.setLayout(self.rightWidget1_down_layout)
        self.rightWidget1_up.setStyleSheet('''#rightWidget1_up{border-image:url(:icons/brief-1-1.jpg);border-radius:10px;}
        ''')

        self.rightWidget1_down.setStyleSheet('''#rightWidget1_down{border-image:url(:icons/briefdown.jpg);
        border-radius:10px;}
        ''')
        # self.rightWidget1_down.setStyleSheet('''#rightWidget1_down{border-left:1px solid darkGray;
        # border-bottom:1px solid darkGray;
        # border-right:1px solid darkGray;border-radius:10px;}''')

        self.filelabel = QtWidgets.QPushButton('')
        self.filelabel.setObjectName('filelabel')






        self.fileline= QtWidgets.QLineEdit()
        self.filelabel2 = QtWidgets.QPushButton('')
        self.filelabel2.setObjectName('filelabel')
        self.rightWidget1_up_layout.addWidget(self.filelabel2)

        self.fileline= QtWidgets.QTextEdit()
        self.fileline.setEnabled(False)
        self.fileline.setFixedHeight(200)
        self.rightWidget1_down_layout.addWidget(self.fileline)
        # lineopacity = QtWidgets.QGraphicsOpacityEffect()
        # lineopacity.setOpacity(0.1)
        # self.fileline.setGraphicsEffect(lineopacity)

        # self.fileline.setBackgroundRole(QtGui.QPalette.ColorRole.Background)
        # self.fileline.setTextBackgroundColor(QtGui.QColor(255,255,0))
        # self.fileline.setAutoFillBackground(True)
        self.fileline.setStyleSheet('margin-left:100px;font-size:20px;color:white;border:none;'
                                    'font-family:"Microsoft Sans Serif", tahoma, arial, "Hiragino Sans GB", 宋体;')
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.ColorRole.Base,QtGui.QColor(255,255,255,0))
        self.fileline.setPalette(palette)


        self.rightWidget5.setShowGrid(False)
        self.rightWidget5.verticalHeader().setVisible(False)

        #窗口1控件样式
        self.rightWidget1.setStyleSheet('''
        #rightWidget1{background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-radius:10px;}
        QLabel#filebtn{
        font-size:16px;
        }
        QPushButton#filelabel{
        border:none;
        color:white;
        font-size:16px;
        height:30px;
        width:150px;
        font-weight:800px;
        }
        
        ''')




        #窗口2设计
        self.rightWidget2_layout = QtWidgets.QGridLayout()
        self.rightWidget2.setLayout(self.rightWidget2_layout)

        #窗口2控件
        self.rightWidget2_aislelabel = QtWidgets.QLabel('通道数:')
        self.rightWidget2_aisleline = QtWidgets.QLineEdit()
        self.rightWidget2_samplelabel = QtWidgets.QLabel('采样率:')
        self.rightWidget2_sampleline = QtWidgets.QLineEdit()
        self.rightWidget2_aisleline.setPlaceholderText('请输入音频通道数:1,2')
        self.rightWidget2_sampleline.setPlaceholderText('请输入音频采样率:默认600')

        #窗口2上下布局
        self.trans_up_layout = QtWidgets.QGridLayout()
        self.trans_down_layout = QtWidgets.QGridLayout()

        self.rightWidget2_layout.addLayout(self.trans_up_layout,0,0,2,6)
        self.rightWidget2_layout.addLayout(self.trans_down_layout,2,0,4,6)

        self.trans_up_layout.addWidget(self.rightWidget2_aislelabel,0,1,1,1,QtCore.Qt.AlignRight)
        self.trans_up_layout.addWidget(self.rightWidget2_aisleline,0,2,1,2)
        self.trans_up_layout.addWidget(self.rightWidget2_samplelabel,1,1,1,1,QtCore.Qt.AlignRight)
        self.trans_up_layout.addWidget(self.rightWidget2_sampleline,1,2,1,2)

        #pcm文件选择
        self.filebtn = QtWidgets.QPushButton()
        self.filebtn.setText('选择文件')
        self.filebtn.setObjectName('filebtn')
        self.filebtn.setStyleSheet('margin-right:30px;')
        # self.rightWidget1_up_layout.addWidget(self.filebtn)
        self.filebtn.setFixedWidth(150)
        self.filebtn.setFixedHeight(30)

        self.filebtn2 = QtWidgets.QPushButton('选择文件夹')
        self.filebtn2.setObjectName('filebtn')
        # self.rightWidget1_up_layout.addWidget(self.filebtn2)
        self.filebtn2.setStyleSheet('margin-right:30px;')
        self.filebtn2.setFixedWidth(150)
        self.filebtn2.setFixedHeight(30)

        self.filebtn.clicked.connect(self.singleFile)
        self.filebtn2.clicked.connect(self.batchFile)

        self.trans_up_layout.addWidget(self.filebtn,0,4,1,1)
        self.trans_up_layout.addWidget(self.filebtn2,1,4,1,1)

        #控件大小设置
        self.rightWidget2_aislelabel.resize(QtCore.QSize(100,30))
        self.rightWidget2_aislelabel.setFont(QtGui.QFont('Tahoma', 16, 25))
        self.rightWidget2_samplelabel.resize(QtCore.QSize(100,30))
        self.rightWidget2_samplelabel.setFont(QtGui.QFont('Tahoma', 16, 25))

        self.rightWidget2_aisleline.setFixedWidth(300)
        self.rightWidget2_sampleline.setFixedWidth(300)
        self.rightWidget2_aisleline.setFixedHeight(30)
        self.rightWidget2_sampleline.setFixedHeight(30)

        self.trans_save_btn = QtWidgets.QToolButton()
        self.trans_save_btn.setText('选择保存路径')
        self.trans_save_btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.trans_save_btn.setIconSize(QtCore.QSize(20,20))
        self.trans_save_btn.setIcon(QtGui.QIcon(':/icons/路径 (1).png'))
        self.trans_save_btn.setFixedWidth(150)
        self.trans_up_layout.addWidget(self.trans_save_btn,2,2,1,1,QtCore.Qt.AlignLeft)
        self.trans_save_btn.setObjectName('trans_btn')

        self.trans_ensure_btn = QtWidgets.QToolButton()
        self.trans_ensure_btn.setText('确认参数')
        self.trans_ensure_btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.trans_ensure_btn.setIconSize(QtCore.QSize(20,20))
        self.trans_ensure_btn.setIcon(QtGui.QIcon(':/icons/确认.png'))
        self.trans_ensure_btn.setFixedWidth(150)
        self.trans_up_layout.addWidget(self.trans_ensure_btn,2,3,1,1,QtCore.Qt.AlignLeft)
        self.trans_ensure_btn.setObjectName('trans_btn')

        self.trans_btn = QtWidgets.QToolButton()
        self.trans_btn.setText('开始转换')
        self.trans_btn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.trans_btn.setIconSize(QtCore.QSize(20,20))
        self.trans_btn.setIcon(QtGui.QIcon(':/icons/开始-default.png'))
        self.trans_btn.setFixedWidth(150)
        self.trans_up_layout.addWidget(self.trans_btn,2,4,1,1,QtCore.Qt.AlignLeft)
        self.trans_btn.setObjectName('trans_btn')

        #下拉菜单
        self.trans_combobox = QtWidgets.QComboBox()
        # self.trans_combobox.setStyleSheet('font-size:16px')
        self.trans_combobox.addItem('处理方式:')
        self.trans_combobox.addItem('单个pcm文件')
        self.trans_combobox.addItem('批量pcm')

        self.trans_combobox.setEnabled(False)
        self.trans_combobox.setFixedWidth(200)
        self.trans_combobox.setFixedHeight(30)
        self.trans_up_layout.addWidget(self.trans_combobox,2,1,1,1,QtCore.Qt.AlignLeft)

        self.trans_text = QtWidgets.QTextEdit()
        self.trans_down_layout.addWidget(self.trans_text)
        self.trans_text.setObjectName('transtext')
        self.trans_text.setEnabled(False)

        self.trans_btn.clicked.connect(self.transFile)
        self.trans_save_btn.clicked.connect(self.transFile)
        self.trans_ensure_btn.clicked.connect(self.transFile)

        self.rightWidget2.setStyleSheet('''
        #rightWidget2{background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-radius:10px;}
        QLabel#filebtn{
        
        font-size:14px;
        }
        QLineEdit{
        border:1px solid gray;
        border-radius:10px;
        padding:2px 4px;
        }
    
        QToolButton{
        border:none;
        color:black;
        font-size:16px;
        height:60px;
        width:150px;
        border-radius:5px;
        }
        QPushButton:hover{
        border:none;
        background:#21A8DF;
        color:white;
        font-size:16px;
        height:60px;
        width:150px;
        border-radius:5px;
        }
        QPushButton#filebtn{
        border:none;
        background:#00bbee;
        color:white;
        font-size:16px;
        height:30px;
        width:150px;
        border-radius:5px;
        }
        QPushButton#filebtn:hover{
        border:none;
        background:#21A8DF;
        
        color:white;
        font-size:16px;
        height:30px;
        width:150px;
        border-radius:5px;
        }
        QTextEdit#transtext{
        background:white;
        font-size:16px;
        color:black;
        border:10px solid #F0F0F0;
        }
        ''')


        #窗口3布局
        self.rightWidget3_layout = QtWidgets.QGridLayout()
        self.rightWidget3.setLayout(self.rightWidget3_layout)

        self.data_tool1 = QtWidgets.QPushButton('单个wav统计')
        self.rightWidget3_layout.addWidget(self.data_tool1,0,0,1,1)
        self.data_tool2 = QtWidgets.QPushButton('多个wav统计')
        self.rightWidget3_layout.addWidget(self.data_tool2,1,0,1,1)
        self.data_tool3 = QtWidgets.QPushButton('新建表格')
        self.rightWidget3_layout.addWidget(self.data_tool3,0,1,1,1)
        self.data_tool4 = QtWidgets.QPushButton('时域统计')
        self.rightWidget3_layout.addWidget(self.data_tool4,1,1,1,1)
        self.data_tool5 = QtWidgets.QPushButton('频域统计')
        self.rightWidget3_layout.addWidget(self.data_tool5,0,2,1,1)
        self.data_tool6 = QtWidgets.QPushButton('绘制频谱')
        self.rightWidget3_layout.addWidget(self.data_tool6,1,2,1,1)
        self.data_tool7 = QtWidgets.QPushButton('窗口及联')
        self.rightWidget3_layout.addWidget(self.data_tool7,0,3,1,1)
        self.data_tool8 = QtWidgets.QPushButton('窗口平铺')
        self.rightWidget3_layout.addWidget(self.data_tool8,1,3,1,1)

        self.data_tool9 = QtWidgets.QTextEdit()
        self.data_tool9.setFixedHeight(70)
        self.data_tool9.setReadOnly(True)
        self.data_tool9.setObjectName('tool9')
        self.data_tool9.setText('未选择wav文件')


        self.rightWidget3_layout.setSpacing(15)
        self.rightWidget3_layout.addWidget(self.data_tool9,0,4,2,1)
        self.data_view = QtWidgets.QMdiArea()
        self.rightWidget3_layout.addWidget(self.data_view,2, 0, 20, 6)
        self.view_count = 0
        #窗口3工具栏

        #窗口3按钮
        # self.data_tool2.clicked.connect(self.dataViewAdd)
        self.data_tool1.clicked.connect(self.dataFile)
        self.data_tool2.clicked.connect(self.dataFile)
        self.data_tool3.clicked.connect(self.dataViewAdd)
        self.data_tool4.clicked.connect(self.dataCope)
        self.data_tool5.clicked.connect(self.dataCope)
        self.data_tool7.clicked.connect(self.dataViewStyle)
        self.data_tool8.clicked.connect(self.dataViewStyle)
        self.data_tool6.clicked.connect(self.dataPaint)


        dataview = QtWidgets.QMdiSubWindow()
        qtabel =QtWidgets.QTableWidget()
        dataview.setWidget(qtabel)
        self.data_view.addSubWindow(dataview)
        dataview.resize(700,500)
        dataview.setWindowTitle('主窗口')
        qtabel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        dataview.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        dataview.customContextMenuRequested.connect(self.dataCustomMenu)
        dataview.show()

        self.rightWidget3.setStyleSheet('''
        #rightWidget3{background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-radius:10px;}

        QPushButton{
        border:none;
        background:#00bbee;
        color:white;
        font-size:14px;
        height:30px;
        width:100px;
        border-radius:5px;
        }
        QPushButton:hover{
        border:none;
        background:#21A8DF;
        color:white;
        font-size:14px;
        height:30px;
        width:150px;
        border-radius:5px;
        }
        QTextEdit#tool9{
        background:#1F1F20;
        font-size:14px;
        color:white;
        border:1px solid #F0F0F0;
        }
        ''')

        #窗口4布局
        self.rightWidget4_layout = QtWidgets.QGridLayout()
        self.rightWidget4.setLayout(self.rightWidget4_layout)

        self.noise_tool1 = QtWidgets.QPushButton('选择文件')
        self.rightWidget4_layout.addWidget(self.noise_tool1,0,1,1,1)
        self.noise_tool2 = QtWidgets.QPushButton('fll滤波')
        self.rightWidget4_layout.addWidget(self.noise_tool2,0,2,1,1)
        self.noise_tool3 = QtWidgets.QPushButton('谱减法滤波')
        self.rightWidget4_layout.addWidget(self.noise_tool3,0,3,1,1)
        self.noise_tool4 = QtWidgets.QPushButton('卡尔曼滤波')
        self.rightWidget4_layout.addWidget(self.noise_tool4,0,4,1,1)

        self.noise_tool5 = QtWidgets.QTextEdit()
        self.noise_tool5.setFixedHeight(60)
        self.noise_tool5.setReadOnly(True)
        self.noise_tool5.setText('未选择wav文件')
        self.noise_tool5.setObjectName('noise_tool5')

        self.rightWidget4_layout.addWidget(self.noise_tool5,0,5,1,1)
        self.noise_view = QtWidgets.QMdiArea()
        self.rightWidget4_layout.addWidget(self.noise_view,1,0,20,6)

        self.noise_tool1.clicked.connect(self.dataFile)

        self.noise_tool2.clicked.connect(self.fllwave)
        self.noise_tool3.clicked.connect(self.wavereduce)
        self.noise_tool4.clicked.connect(self.karmanwave)




        self.rightWidget4.setStyleSheet('''
        #rightWidget4{background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-radius:10px;}
        QPushButton{
        border:none;
        background:#27D018;
        color:white;
        height:30px;
        width:100px;
        font-size:14px;
        border-radius:5px;
        }
        QPushButton:hover{
        border:none;
        background:green;
        color:white;
        font-size:14px;
        border-radius:5px;
        }
        QPushButton{
        border:none;
        background:#00bbee;
        color:white;
        font-size:16px;
        height:30px;
        width:100px;
        border-radius:5px;
        }
        QPushButton:hover{
        border:none;
        background:#21A8DF;
        color:white;
        font-size:16px;
        height:30px;
        width:150px;
        border-radius:5px;
        }
        QTextEdit#noise_tool5{
        background:#1F1F20;
        font-size:14px;
        color:white;
        border:1px solid #F0F0F0;
        }
        ''')
        #窗口5布局
        self.rightWidget5.setColumnCount(4)
        self.rightWidget5.setHorizontalHeaderLabels(['文件名', '时间', '模块', ''])
        self.rightWidget5.setColumnWidth(1, 300)
        self.rightWidget5.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.rightWidget5.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.rightWidget5.customContextMenuRequested.connect(self.saveMenu)

        self.rightWidget5.setStyleSheet('''
                #rightWidget5{background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-radius:10px;
                font-size:14px;
                font-family:SimSun,Tahoma;
                }
                QPushButton{
                border:none;
                background:#27D018;
                color:white;
                font-size:14px;
                border-radius:5px;
                }
                QPushButton:hover{
                border:none;
                background:green;
                color:white;
                font-size:14px;
                border-radius:5px;
                }

                ''')

        #窗口6设计
        self.rightWidget6_layout = QtWidgets.QGridLayout()
        self.rightWidget6.setLayout(self.rightWidget6_layout)
        self.rightWidget6_up_widget = QtWidgets.QWidget()
        self.rightWidget6_mid_widget = QtWidgets.QWidget()
        self.rightWidget6_down_widget = QtWidgets.QWidget()
        self.rightWidget6_layout.addWidget(self.rightWidget6_up_widget,0,0,1,10)
        self.rightWidget6_layout.addWidget(self.rightWidget6_mid_widget,1,0,1,10)
        self.rightWidget6_layout.addWidget(self.rightWidget6_down_widget,2,0,10,10)
        self.rightWidget6_up_widget_layout = QtWidgets.QHBoxLayout()
        self.rightWidget6_up_widget.setLayout(self.rightWidget6_up_widget_layout)
        self.rightWidget6_up_widget.setObjectName('rightWidget6_up_widget')
        self.rightWidget6_layout.setContentsMargins(0,0,0,0)
        self.rightWidget6_mid_widget_layout = QtWidgets.QHBoxLayout()
        self.rightWidget6_mid_widget.setLayout(self.rightWidget6_mid_widget_layout)

        self.rightWidget6_up_widget_btn1 = QtWidgets.QPushButton(self.rightWidget6_up_widget)
        self.rightWidget6_up_widget_btn1.setText('音频重采样')
        self.rightWidget6_up_widget_layout.addWidget(self.rightWidget6_up_widget_btn1)
        self.rightWidget6_up_widget_btn2 = QtWidgets.QPushButton(self.rightWidget6_up_widget)
        self.rightWidget6_up_widget_btn2.setText('增加噪音')
        self.rightWidget6_up_widget_layout.addWidget(self.rightWidget6_up_widget_btn2)
        self.rightWidget6_up_widget_btn3 = QtWidgets.QPushButton(self.rightWidget6_up_widget)
        self.rightWidget6_up_widget_btn3.setText('模型降噪')
        self.rightWidget6_up_widget_layout.addWidget(self.rightWidget6_up_widget_btn3)

        self.rightWidget6_up_widget_btn1.clicked.connect(self.resampleWav)
        self.rightWidget6_up_widget_btn2.clicked.connect(self.sub_add_Noise)
        self.rightWidget6_up_widget_btn3.clicked.connect(self.createModel)

        self.rightWidget6_mid_widget_processbar = QtWidgets.QProgressBar()
        self.rightWidget6_mid_widget_layout.addWidget(self.rightWidget6_mid_widget_processbar)
        self.rightWidget6_mid_widget_processbar.setFixedWidth(200)
        self.rightWidget6_mid_widget_processbar.setMinimumHeight(30)
        self.rightWidget6_mid_widget_processbar.setValue(0)

        self.rightWidget6_down_widget_layout = QtWidgets.QHBoxLayout()


        self.rightWidget6_down_widget_layout_w1 = QtWidgets.QTextEdit()
        self.rightWidget6_down_widget_layout.addWidget(self.rightWidget6_down_widget_layout_w1)
        self.rightWidget6_down_widget_layout_w1.setEnabled(False)
        self.rightWidget6_down_widget_layout_w2 = QtWidgets.QTextEdit()
        self.rightWidget6_down_widget_layout.addWidget(self.rightWidget6_down_widget_layout_w2)
        self.rightWidget6_down_widget_layout_w2.setEnabled(False)
        self.rightWidget6_down_widget_layout_w3 = QtWidgets.QTextEdit()
        self.rightWidget6_down_widget_layout.addWidget(self.rightWidget6_down_widget_layout_w3)
        self.rightWidget6_down_widget_layout_w3.setEnabled(False)
        self.rightWidget6_down_widget_layout_w1.setFixedHeight(300)
        self.rightWidget6_down_widget_layout_w2.setFixedHeight(300)
        self.rightWidget6_down_widget_layout_w3.setFixedHeight(300)
        self.rightWidget6_down_widget_layout.setAlignment(self.rightWidget6_down_widget_layout_w1,QtCore.Qt.AlignTop)
        self.rightWidget6_down_widget_layout.setAlignment(self.rightWidget6_down_widget_layout_w2,QtCore.Qt.AlignTop)
        self.rightWidget6_down_widget_layout.setAlignment(self.rightWidget6_down_widget_layout_w3,QtCore.Qt.AlignTop)
        self.rightWidget6_down_widget.setLayout(self.rightWidget6_down_widget_layout)


        self.rightWidget6_down_widget_layout_w1.setText('音频采样模块：')
        self.rightWidget6_down_widget_layout_w1.append('用于将待处理音频和噪音重采样到同一音频，便于处理。')
        self.rightWidget6_down_widget_layout_w1.append('输出频率为16000效果较好。')
        self.rightWidget6_down_widget_layout_w1.append('输入通道数不能大于2。')
        self.rightWidget6_down_widget_layout_w1.append('输入输出路径不能相同。')
        self.rightWidget6_down_widget_layout_w1.append(
            '--------------\n举例：\n输入路径：./data/\n输出路径：./data1/\n输出采样率：16000')

        self.rightWidget6_down_widget_layout_w2.setText('音频加噪模块：')
        self.rightWidget6_down_widget_layout_w2.append('用于给原始声纳增加噪声。')
        self.rightWidget6_down_widget_layout_w2.append('保持噪声和原始音频同样采样率。')
        self.rightWidget6_down_widget_layout_w2.append('噪声路径必须是单个文件。')
        self.rightWidget6_down_widget_layout_w2.append(
            '--------------\n举例：\n输入原始路径：./data/\n输入噪声路径：./data1/noise1.wav\n输出路径：./noisy/')

        self.rightWidget6_down_widget_layout_w3.setText('去噪模型：')
        self.rightWidget6_down_widget_layout_w3.append('用于给原始声纳去除噪声。')
        self.rightWidget6_down_widget_layout_w3.append('输入待去噪文件路径，文件格式必须是16000的频率。')



        self.rightWidget6.setStyleSheet('''
        #rightWidget6{background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-radius:10px;
        font-size:14px;
        }
        ''')
        self.rightWidget6_up_widget.setStyleSheet('''
        #rightWidget6_up_widget{
        background:#0A071A;
          
        }
        QPushButton{
        font-size:16px;
        background:#0A071A;
        color:#6F6D7D;
        }
        QPushButton:hover{
        
        color:white;
        }
        ''')

    def addNoise(self,widget,line_cleanpath,line_noisepath,line_noisypath,line_snr):
        if os.path.exists(line_cleanpath) and os.path.exists(line_noisepath) and os.path.exists(line_noisypath):
            if os.path.exists(line_snr):
                self.rightWidget6_down_widget_layout_w2.setText('')
                files = os.listdir(line_noisypath)
                length = len(files)
                self.rightWidget6_down_widget_layout_w2.append(f'{line_noisypath}中，共%d个文件加噪完成！'%length)
                widget.close()
                addNoise(line_cleanpath,line_noisepath,int(line_snr),line_noisypath)

            else:
                QtWidgets.QMessageBox.information(self,'信息提示','未设置信噪比!')
        else:
            QtWidgets.QMessageBox.information(self,'信息提示','路径设置错误!')

    def sub_add_Noise(self):
        #窗口6 增加噪声
        widget = QtWidgets.QDialog()
        layout = QtWidgets.QFormLayout()
        line_cleanpath = QtWidgets.QLineEdit()
        layout.addRow('原始文件路径：',line_cleanpath)
        line_noisepath = QtWidgets.QLineEdit()
        layout.addRow('带噪文件路径：',line_noisepath)
        line_noisypath = QtWidgets.QLineEdit()
        layout.addRow('输出文件路径：',line_noisypath)

        line_snr = QtWidgets.QLineEdit()
        line_snr.setText('5')
        layout.addRow('生成音频信噪比：',line_snr)
        btn = QtWidgets.QPushButton('确定')
        layout.addWidget(btn)
        widget.setLayout(layout)
        btn.clicked.connect(lambda :self.addNoise(widget,line_cleanpath.text(),line_noisepath.text(),line_noisypath.text(),line_snr.text()))

        widget.exec_()


    def applyModel(self,w,clean_path,noisy_path,bar,edit):
        if os.path.exists(noisy_path) :
            if os.path.exists(clean_path) or clean_path=='':

                sonaModel.main(clean_path,noisy_path,bar,edit)

                w.close()

                #
            else:
                QtWidgets.QMessageBox.information(self,'信息提示','原始路径格式错误！')
        else:
            QtWidgets.QMessageBox.information(self,'信息提示','噪音路径缺失！')
    def createModel(self):

        #窗口6 建模
        widget = QtWidgets.QDialog()
        layout = QtWidgets.QFormLayout()
        line_cleanpath = QtWidgets.QLineEdit()
        layout.addRow('原始文件路径：',line_cleanpath)
        line_noisypath = QtWidgets.QLineEdit()
        layout.addRow('带躁文件路径：',line_noisypath)
        line_noisypath.setText('./noisy/')
        btn = QtWidgets.QPushButton('确定')
        bar = QtWidgets.QProgressBar(widget)
        edit = QtWidgets.QTextEdit(widget)
        edit.setEnabled(False)
        layout.addWidget(bar)
        layout.addWidget(edit)
        layout.addWidget(btn)
        widget.setLayout(layout)

        btn.clicked.connect(lambda :self.applyModel(widget,line_cleanpath.text(),line_noisypath.text(),bar,edit))

        widget.exec_()

    def sub_sample_param(self,w,line_filepath,line_outrate,outpath):

            if os.path.exists(line_filepath) and os.path.exists(outpath) and line_outrate != '':
                ok,i = batch_sample.resample(line_filepath,line_outrate,outpath)
                if ok == 'waverror':
                    QtWidgets.QMessageBox.information(self,'信息提示',f'{i}音频受损!')
                elif ok == 'patherror':
                    QtWidgets.QMessageBox.information(self,'信息提示','此音频通道数大于2!')
                else:
                    self.rightWidget6_down_widget_layout_w1.setText('')
                    self.rightWidget6_down_widget_layout_w1.append(f'输入文件路径：{line_filepath}。')
                    self.rightWidget6_down_widget_layout_w1.append(f'输出采样率：{line_outrate}。')
                    self.rightWidget6_down_widget_layout_w1.append(f'输出路径：{outpath}。')
                    self.rightWidget6_down_widget_layout_w1.append(f'重采样完成！')

                    w.close()

            else:
                QtWidgets.QMessageBox.information(self,'信息提示','不存在路径或未设置采样率!')


    def resampleWav(self):
        #窗口6重采样
        widget = QtWidgets.QDialog()
        layout = QtWidgets.QFormLayout()
        line_filepath = QtWidgets.QLineEdit()
        layout.addRow('输入文件路径：',line_filepath)
        line_filepath_out = QtWidgets.QLineEdit()
        layout.addRow('输出文件路径：',line_filepath_out)

        line_outrate = QtWidgets.QLineEdit()
        layout.addRow('输出文件的采样率：',line_outrate)
        btn = QtWidgets.QPushButton('确定')
        layout.addWidget(btn)
        widget.setLayout(layout)
        btn.clicked.connect(lambda :self.sub_sample_param(widget,line_filepath.text(),line_outrate.text(),line_filepath_out.text()))

        widget.exec_()


    def karmanwave(self):
        subwidget = QtWidgets.QMdiSubWindow()
        subwidget.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        subwidget.resize(600,450)

        removewidget = QtWidgets.QWidget()
        remove_layout = QtWidgets.QFormLayout()
        removewidget.setLayout(remove_layout)
        subwidget.setWidget(removewidget)
        self.noise_view.addSubWindow(subwidget)

        removewidget.setWindowTitle('卡尔曼滤波')

        remove_scale0 = QtWidgets.QLineEdit()
        # remove_scale_valid0 = QtGui.QDoubleValidator()
        # remove_scale_valid0.setRange(0.0001,0.01)
        # remove_scale0.setValidator(remove_scale_valid0)
        remove_layout.addRow('状态矩阵：',remove_scale0)
        remove_scale0.setPlaceholderText('默认:0.01')

        remove_scale = QtWidgets.QLineEdit()
        remove_scale_valid = QtGui.QIntValidator()
        remove_scale_valid.setRange(0,100)
        remove_scale.setValidator(remove_scale_valid)
        remove_layout.addRow('样本比例：',remove_scale)
        remove_scale.setPlaceholderText('0-100')



        remove_textEdit = QtWidgets.QTextEdit()
        remove_layout.addRow(remove_textEdit)
        remove_textEdit.setFixedWidth(250)
        remove_textEdit.setFixedHeight(150)

        remove_btn_param = QtWidgets.QPushButton('确认参数')
        remove_layout.addRow(remove_btn_param)
        remove_btn_param.setFixedWidth(150)

        remove_btn_renoise = QtWidgets.QPushButton('卡尔曼滤波')
        remove_layout.addRow(remove_btn_renoise)
        remove_btn_renoise.setFixedWidth(150)

        remove_btn_save = QtWidgets.QPushButton('保存文件')
        remove_layout.addRow(remove_btn_save)
        remove_btn_save.setFixedWidth(150)

        remove_btn_param.clicked.connect(self.karmansure)
        remove_btn_renoise.clicked.connect(self.karmannoise)
        # remove_btn_save.clicked.connect()
        removewidget.show()

    def karmansave(self):
        if not self.noisefile:
            return
        karman_path = QtWidgets.QFileDialog.getSaveFileName(None,'保存',os.getcwd(),'.WAV(*.wav)')
        karman_path = karman_path[0]
        if not karman_path:return
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        value = float(child.findChildren(QtWidgets.QLineEdit)[0].text())
        textedit = child.findChild(QtWidgets.QTextEdit)
        if not textedit.toPlainText():
            QtWidgets.QMessageBox.information(self,'信息提示','未确认参数!')
            return
        _,_,data = karmanfilter(self.noisefile,value,100)
        ffl_obj = ffl.FflNoise(self.noisefile)
        ffl_obj.ffl_save(data,karman_path)

    def karmannoise(self):
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        value = float(child.findChildren(QtWidgets.QLineEdit)[0].text())
        scale = int(child.findChildren(QtWidgets.QLineEdit)[1].text())
        textedit = child.findChild(QtWidgets.QTextEdit)
        if not textedit.toPlainText():
            QtWidgets.QMessageBox.information(self,'信息提示','未确认参数!')
            return
        times,sigs,data = karmanfilter(self.noisefile,value,scale)
        self.noise_paint(times,sigs,data)

    def karmansure(self):
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]

        value =child.findChildren(QtWidgets.QLineEdit)[0].text()
        scale =child.findChildren(QtWidgets.QLineEdit)[1].text()
        textedit = child.findChild(QtWidgets.QTextEdit)
        if  not self.noisefile or not scale or not value:
            QtWidgets.QMessageBox.information(self,'信息提示','未选取参数或文件!')
            return
        textedit.setText('')
        textedit.append(f'选取的文件是:{self.noisefile.split("/")[-1]}。\n')
        textedit.append(f'降噪方式为：卡尔曼滤波。\n')
        textedit.append(f'状态参数取值：{value}\n')
        textedit.append(f'选取的显示比例是：{scale}\n')

    def wavereduce(self):
        subwidget = QtWidgets.QMdiSubWindow()
        subwidget.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        subwidget.resize(600,450)

        removewidget = QtWidgets.QWidget()
        remove_layout = QtWidgets.QFormLayout()
        removewidget.setLayout(remove_layout)
        subwidget.setWidget(removewidget)
        self.noise_view.addSubWindow(subwidget)

        removewidget.setWindowTitle('谱减法滤波')

        remove_scale = QtWidgets.QLineEdit()
        remove_scale_valid = QtGui.QIntValidator()
        remove_scale_valid.setRange(0,100)
        remove_layout.addRow('样本比例：',remove_scale)
        remove_scale.setValidator(remove_scale_valid)
        remove_scale.setPlaceholderText('要显示的样本比例：0-100')

        remove_textEdit = QtWidgets.QTextEdit()
        remove_layout.addRow(remove_textEdit)
        remove_textEdit.setFixedWidth(250)
        remove_textEdit.setFixedHeight(150)

        remove_btn_param = QtWidgets.QPushButton('确认参数')
        remove_layout.addRow(remove_btn_param)
        remove_btn_param.setFixedWidth(150)

        remove_btn_renoise = QtWidgets.QPushButton('谱减降噪')
        remove_layout.addRow(remove_btn_renoise)
        remove_btn_renoise.setFixedWidth(150)

        remove_btn_save = QtWidgets.QPushButton('保存文件')
        remove_layout.addRow(remove_btn_save)
        remove_btn_save.setFixedWidth(150)

        remove_btn_param.clicked.connect(self.reducesure)
        remove_btn_renoise.clicked.connect(self.reducenoise)
        remove_btn_save.clicked.connect(self.reducesave)
        removewidget.show()

    def reducesave(self):
        if not self.noisefile:
            return
        reducesave_path = QtWidgets.QFileDialog.getSaveFileName(None,'保存',os.getcwd(),'.WAV(*.wav)')
        reducesave_path = reducesave_path[0]
        if not reducesave_path:return

        wave = self.noisefile
        data = wavereduce(wave)
        ffl_obj = ffl.FflNoise(self.noisefile)
        times,sigs = ffl_obj.get_sigs()
        lenth = len(data.shape)
        if lenth>1:
            data = data.reshape(-1)
        lt = len(times)
        ld = len(data)
        if lt> ld:
            num = lt - ld
            for i in range(num):
                data = np.append(data,0)
        elif lt<ld:
            data = data[:lt]
        ffl_obj.ffl_save(data,reducesave_path)
    def reducenoise(self):
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        text = child.findChild(QtWidgets.QTextEdit).toPlainText()
        if not text:
            QtWidgets.QMessageBox.information(self,'信息提示','未确认参数!')
            return
        scale = child.findChild(QtWidgets.QLineEdit).text()
        scale = int(scale)

        wave = self.noisefile
        data = wavereduce(wave)
        ffl_obj = ffl.FflNoise(self.noisefile)
        times,sigs = ffl_obj.get_sigs()
        lenth = len(data.shape)
        if lenth>1:
            data = data.reshape(-1)
        lt = len(times)
        ld = len(data)
        if lt> ld:
            num = lt - ld
            for i in range(num):
                data = np.append(data,0)
        elif lt<ld:
            data = data[:lt]

        scale = int(lt*scale/100)
        data = data/(2**15)
        self.noise_paint(times[:scale],sigs[:scale],data[:scale])

    def reducesure(self):


        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        # child = child.children()
        scale = child.findChild(QtWidgets.QLineEdit).text()
        if  not self.noisefile or not scale:
            QtWidgets.QMessageBox.information(self,'信息提示','未选取参数或文件!')
            return

        textedit = child.findChild(QtWidgets.QTextEdit)
        textedit.setText('')

        textedit.append(f'选取的文件是:{self.noisefile.split("/")[-1]}。\n')
        textedit.append(f'降噪方式为：谱减法滤波。\n')
        textedit.append(f'选取的显示比例是：{scale}')

    def fllwave(self):
            #傅立叶窗口布局
            subwidget = QtWidgets.QMdiSubWindow()
            subwidget.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
            subwidget.resize(600,500)

            fllwidget = QtWidgets.QTabWidget()
            subwidget.setWidget(fllwidget)
            self.noise_view.addSubWindow(subwidget)



            fllwidget.setWindowTitle('傅立叶滤波')

            tab1 = QtWidgets.QWidget()
            tab2 = QtWidgets.QWidget()
            tab3 = QtWidgets.QWidget()

            fllwidget.addTab(tab1,'阈值滤波')
            fllwidget.addTab(tab2,'中值滤波')
            fllwidget.addTab(tab3,'均值滤波')

            tab1_layout = QtWidgets.QFormLayout()
            tab1.setLayout(tab1_layout)
            tab2_layout = QtWidgets.QFormLayout()
            tab2.setLayout(tab2_layout)
            tab3_layout = QtWidgets.QFormLayout()
            tab3.setLayout(tab3_layout)

            #tab3设置

            tab3_combebox = QtWidgets.QComboBox()
            # tab2_combebox.addItem('未选择方式')
            tab3_combebox.addItem('均值滤波')
            tab3_combebox.setEnabled(False)
            tab3_layout.addRow(tab3_combebox)
            tab3_combebox.setFixedWidth(200)

            tab3_value = QtWidgets.QLineEdit()
            tab3_valid = QtGui.QIntValidator()
            tab3_layout.addRow('样本个数：',tab3_value)
            tab3_value.setValidator(tab3_valid)
            tab3_value.setPlaceholderText('要显示的样本比例：0-100')

            tab3_text1 = QtWidgets.QTextEdit()
            tab3_layout.addRow(tab3_text1)
            tab3_text1.setFixedWidth(300)
            tab3_text1.setFixedHeight(150)

            tab3_btn1 = QtWidgets.QPushButton('确认参数')
            tab3_layout.addRow(tab3_btn1)
            tab3_btn1.setFixedWidth(150)
            tab3_btn1.clicked.connect(self.tab2_sure)

            tab3_btn2 = QtWidgets.QPushButton('统计降噪')
            tab3_layout.addRow(tab3_btn2)
            tab3_btn2.setFixedWidth(150)
            tab3_btn2.clicked.connect(self.tab_noise)

            tab3_btn_save = QtWidgets.QPushButton('保存文件')
            tab3_layout.addRow(tab3_btn_save)
            tab3_btn_save.setFixedWidth(150)
            tab3_btn_save.clicked.connect(self.fflsave)

            #tab2设置

            tab2_combebox = QtWidgets.QComboBox()
            # tab2_combebox.addItem('未选择方式')
            tab2_combebox.addItem('中值滤波')

            tab2_combebox.setEnabled(False)
            tab2_layout.addRow(tab2_combebox)
            tab2_combebox.setFixedWidth(200)

            tab2_value = QtWidgets.QLineEdit()
            tab2_valid = QtGui.QIntValidator()
            tab2_layout.addRow('样本个数：',tab2_value)
            tab2_value.setValidator(tab2_valid)
            tab2_value.setPlaceholderText('要显示的样本比例：0-100')

            tab2_text1 = QtWidgets.QTextEdit()
            tab2_layout.addRow(tab2_text1)
            tab2_text1.setFixedWidth(300)
            tab2_text1.setFixedHeight(150)

            tab2_btn1 = QtWidgets.QPushButton('确认参数')
            tab2_layout.addRow(tab2_btn1)
            tab2_btn1.setFixedWidth(150)
            tab2_btn1.clicked.connect(self.tab2_sure)

            tab2_btn2 = QtWidgets.QPushButton('统计降噪')
            tab2_layout.addRow(tab2_btn2)
            tab2_btn2.setFixedWidth(150)
            tab2_btn2.clicked.connect(self.tab_noise)

            tab2_btn_save = QtWidgets.QPushButton('保存文件')
            tab2_layout.addRow(tab2_btn_save)
            tab2_btn_save.setFixedWidth(150)
            tab2_btn_save.clicked.connect(self.fflsave)

            # tab1 设置
            tab1_combebox = QtWidgets.QComboBox()

            tab1_combebox.addItem('自定义频率')
            tab1_layout.addRow(tab1_combebox)
            tab1_combebox.setFixedWidth(200)
            tab1_combebox.setEnabled(False)

            tab1_text1 = QtWidgets.QTextEdit()
            tab1_layout.addRow(tab1_text1)
            tab1_text1.setFixedWidth(300)
            tab1_text1.setFixedHeight(150)


            tab1_value1 = QtWidgets.QLineEdit()
            tab1_valid = QtGui.QIntValidator()
            tab1_valid.setRange(0,100)
            tab1_layout.addRow('滤波阈值：',tab1_value1)
            tab1_value1.setValidator(tab1_valid)
            tab1_value1.setPlaceholderText('保存高频比例:0-100')

            tab1_value2 = QtWidgets.QLineEdit()
            tab1_valid2 = QtGui.QIntValidator()
            tab1_layout.addRow('样本个数：',tab1_value2)
            tab1_value2.setValidator(tab1_valid2)
            tab1_value2.setPlaceholderText('要显示的样本比例:0-100')

            tab0_btn = QtWidgets.QPushButton('确认参数')
            tab1_layout.addRow(tab0_btn)
            tab0_btn.setFixedWidth(150)
            tab0_btn.clicked.connect(self.tab1_sure)

            tab1_btn = QtWidgets.QPushButton('频率降噪')
            tab1_layout.addRow(tab1_btn)
            tab1_btn.setFixedWidth(150)
            tab1_btn.clicked.connect(self.tab_noise)

            tab1_btn_save = QtWidgets.QPushButton('保存文件')
            tab1_layout.addRow(tab1_btn_save)
            tab1_btn_save.setFixedWidth(150)
            tab1_btn_save.clicked.connect( self.fflsave)




            fllwidget.show()

    def fflsave(self):
        if not self.noisefile:
            return
        fflsave_path = QtWidgets.QFileDialog.getSaveFileName(None,'保存',os.getcwd(),'.WAV(*.wav)')
        fflsave_path = fflsave_path[0]
        if not fflsave_path:return
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        child = child.children()
        child = child[0].currentWidget()
        btn = child.findChildren(QtWidgets.QPushButton)[1]
        text = btn.text()


        filename = fflsave_path.split('/')[-1]
        ffl_obj = ffl.FflNoise(self.noisefile)

        if text == '统计降噪':
            idx = child.findChildren(QtWidgets.QComboBox)[0].currentIndex()

            if idx == 1:

                _,_,filters = ffl_obj.medianffl(100)
                ffl_obj.ffl_save(filters,fflsave_path)
                self.noise_tool5.setText('已保存文件:'+filename+'!')
            else:

                _,_,filters = ffl_obj.meanffl(100)
                ffl_obj.ffl_save(filters,fflsave_path)
                self.noise_tool5.setText('已保存文件:'+filename+'!')
        else:
            line1 = child.findChildren(QtWidgets.QLineEdit)[0].text()
            _,_,filters = ffl_obj.ffl(100,int(line1))
            ffl_obj.ffl_save(filters,fflsave_path)
            self.noise_tool5.setText('已保存文件:'+filename+'!')


    def tab_noise(self):
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        child = child.children()
        child = child[0].currentWidget().children()

        type = self.sender().text()


        ffl_obj = ffl.FflNoise(self.noisefile)

        if type == '统计降噪':
            idx = child[1].currentText()
            scale2 = child[-5].text()
            text = child[-4].toPlainText()
            if not text:

                QtWidgets.QMessageBox.information(self,'信息提示','未确认参数!')
                return
            if idx == '中值滤波':

                times,sigs,filters = ffl_obj.medianffl(int(scale2))
                self.noise_paint(times,sigs,filters)


            else:
                times,sigs,filters = ffl_obj.meanffl(int(scale2))
                self.noise_paint(times,sigs,filters)
        else:
            text = child[2].toPlainText()
            if not text:
                QtWidgets.QMessageBox.information(self,'信息提示','未确认参数!')
                return
            scale1 = child[-4].text()
            value = child[-6].text()
            item = ffl_obj.ffl(int(scale1),value)
            times,sigs,filters =item
            self.noise_paint(times,sigs,filters)

    def tab2_sure(self):
        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        child = child.children()
        child = child[0].currentWidget().children()


        scale = child[-5].text()
        if  not self.noisefile or not scale:
            QtWidgets.QMessageBox.information(self,'信息提示','未选取参数或文件!')
            return
        ffl_obj = ffl.FflNoise(self.noisefile)
        file = self.noisefile.split('/')[-1]
        text = child[1].currentText()
        child[-4].setText('')
        child[-4].append(f'选择的文件是：{file}。\n')
        child[-4].append(f'选择的方式是：{text}。\n')
        child[-4].append(f'选择的显示个数是：{scale}。\n')
        if text == '中值滤波':
            median = ffl_obj.median
            child[-4].append(f'当前中值为：{median}。\n')
        else:
            mean = ffl_obj.mean
            child[-4].append(f'当前均值为：{mean}。\n')


    def noise_paint(self,times,sigs,filters):
        plt.rcParams["font.family"] = 'Arial Unicode MS'
        figure = plt.figure(num="频谱图",figsize=(9,6))

        ax = plt.subplot(2,1,1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times,sigs,label='降噪前')
        plt.legend()
        plt.title('降噪前时域谱',fontsize = 16)


        ax = plt.subplot(2,1,2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times,filters,label='降噪前')
        plt.legend()
        plt.title('降噪后时域谱',fontsize = 16)

        plt.tight_layout()

        plt.show()
        figure.clf()
        plt.close()
        gc.collect()
    def tab1_sure(self):

        subw = self.noise_view.currentSubWindow()
        child = subw.children()[-1]
        child = child.children()
        child = child[0].currentWidget().children()

        value = child[-6].text()
        scale = child[-4].text()

        if not value or not scale or not self.noisefile:
            QtWidgets.QMessageBox.information(self,'信息提示','未选取参数或文件!')
            return
        ffl_obj = ffl.FflNoise(self.noisefile)
        item = ffl_obj.get_freq(value)
        file = self.noisefile.split('/')[-1]
        child[2].setText('')
        child[2].append(f'选择的文件是：{file}。\n')
        child[2].append('选择的方式是：自定义频率。\n')
        child[2].append(f'选择的阈值是：{value}。\n')
        child[2].append(f'选择的显示个数是：{scale}。\n')
        child[2].append(f'频率个数：{len(item)}。\n')
        child[2].append(f'频率分布：{item}。\n')



    def dataPaint2(self,item):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
        plt.rcParams['axes.unicode_minus'] = False

        sigs0 = item[0]

        ceps0 = item[1]
        times = item[2]
        freqs0 = item[3]

        sigs1 = item[4]
        ceps1 = item[5]
        freqs1 = item[6]

        freqs = item[7]
        pows = item[8]
        sigs = item[9]
        times_all = item[10]

        sigs_0 = 10*log10((sigs0*(2**15))**2)
        sigs_1 = 10*log10((sigs1*(2**15))**2)


        figure = plt.figure(num="频谱图",figsize=(9,6))
        ax = plt.subplot(4,2,1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times,sigs0,label = 'elec')
        plt.legend()
        plt.title('左时域谱')

        ax = plt.subplot(4,2,2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times,sigs1,label = 'elec')
        plt.legend()
        plt.title('右时域谱')

        ax = plt.subplot(4,2,3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times_all,sigs,label = 'elec')
        plt.legend()
        plt.title('时域图')



        ax = plt.subplot(4,2,4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('频率(Hz)')
        plt.ylabel('幅值')

        scale = sorted(pows)[-2]
        plt.ylim(0,scale)
        plt.plot(freqs,pows,label = 'amplitude',color = 'green')
        plt.legend()

        plt.title('频谱图')

        ax = plt.subplot(4,2,5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('幅值')
        plt.plot(times,sigs_0,label = 'elec')
        plt.legend()
        # plt.ylim(0,0.02)
        plt.title('左功率谱')

        ax = plt.subplot(4,2,6)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('幅值')
        plt.plot(times,sigs_1,label = 'elec')
        plt.legend()
        # plt.ylim(0,0.02)
        plt.title('右功率谱')

        ax = plt.subplot(4,2,7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('频率(Hz)')
        plt.ylabel('幅值')
        plt.plot(freqs0,ceps0,label = 'amplitude',color = 'green')
        plt.legend()
        plt.title('倒频谱')

        ax = plt.subplot(4,2,8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('频率(Hz)')
        plt.ylabel('幅值')
        plt.plot(freqs1,ceps1,label = 'amplitude',color = 'green')
        plt.legend()
        plt.title('倒频谱')

        plt.tight_layout()

        plt.show()
        figure.clf()
        plt.close()
        gc.collect()
    def dataPaint1(self,sigs,times,freqs,pows,ceps):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
        plt.rcParams['axes.unicode_minus'] = False

        sigs_ = 10*log10((sigs*(2**15))**2)
        figure = plt.figure(num="频谱图",figsize=(9,6))
        ax = plt.subplot(2,2,1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('电压(V)')
        plt.plot(times,sigs,label = 'elec')
        plt.legend()
        plt.title('时域谱')

        ax = plt.subplot(2,2,2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('时间(S)')
        plt.ylabel('幅值')
        plt.plot(times,sigs_,label = 'elec')
        plt.legend()

        plt.title('功率谱')

        ax = plt.subplot(2,2,3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('频率(Hz)')
        plt.ylabel('幅值')
        plt.plot(freqs,pows,label = 'amplitude',color = 'green')
        plt.legend()
        plt.title('频谱图')

        ax = plt.subplot(2,2,4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel('频率(Hz)')
        plt.ylabel('幅值')
        plt.plot(freqs,ceps,label = 'amplitude',color = 'green')
        plt.legend()
        plt.title('倒频谱')

        plt.tight_layout()

        plt.show()
        figure.clf()
        plt.close()
        gc.collect()
    def dataPaint(self):

        window = self.data_view.currentSubWindow()
        qtabel = window.children()[-1]
        row = qtabel.currentRow()
        item = qtabel.item(row,0)
        if not item:
            return

        # dataview = QtWidgets.QMdiSubWindow()
        # tabel =QtWidgets.QWidget()
        # dataview.setWidget(tabel)
        # self.data_view.addSubWindow(dataview)
        # dataview.resize(1000,600)
        # dataview.setWindowTitle('主窗口')
        # dataview.show()

        #时频绘图
        data = analysisdata.DataAnalysis(item.text())
        aisle = data.getAisle()
        if aisle == 1:
            sigs,times,freqs,pows,ceps = data.get_data()

            self.dataPaint1(sigs,times,freqs,pows,ceps )
        else:
            item = data.get_data()
            self.dataPaint2(item)





    def dataViewStyle(self):
        text = self.sender().text()
        if text == '窗口及联':
            self.data_view.cascadeSubWindows()
        else:
            self.data_view.tileSubWindows()

    def dataViewAdd(self):
        self.view_count += 1

        dataview = QtWidgets.QMdiSubWindow()
        dataview.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        qtabel =QtWidgets.QTableWidget()

        dataview.setWidget(qtabel)
        self.data_view.addSubWindow(dataview)
        dataview.resize(700,500)
        dataview.setWindowTitle('窗口'+str(self.view_count))
        dataview.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        dataview.customContextMenuRequested.connect(self.dataCustomMenu)
        qtabel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        qtabel.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        qtabel.setSortingEnabled(False)
        dataview.show()




    def dataCustomMenu(self,pos):
        menu = QtWidgets.QMenu()

        menu.addAction('复制')
        menu.addAction('最大值')
        menu.addAction('最小值')
        menu.addAction('删除')
        menu.addAction('升序')
        menu.addAction('降序')


        window = self.data_view.currentSubWindow()
        qtabel = window.children()[-1]
        p = qtabel.mapToGlobal(pos)
        action = menu.exec(p)
        if action:
            text = action.text()
            if text == '升序':
                col = qtabel.currentColumn()
                qtabel.sortByColumn(col,QtCore.Qt.SortOrder.AscendingOrder)
            elif text == '降序':
                col = qtabel.currentColumn()
                qtabel.sortByColumn(col,QtCore.Qt.SortOrder.DescendingOrder)
            elif text == '最大值':
                row = qtabel.currentRow()
                row_num = qtabel.rowCount()
                col = qtabel.currentColumn()

                if col<5:
                    return
                items = []
                for i in range(row_num):
                    item = qtabel.item(i,col)
                    if item:
                        items.append(float(item.text()))
                if items:
                    index = items.index(max(items))
                    qtabel.item(index,col).setForeground(QtGui.QBrush(QtCore.Qt.red))

            elif text == '最小值':
                row = qtabel.currentRow()
                row_num = qtabel.rowCount()
                col = qtabel.currentColumn()

                if col<5:
                    return
                items = []
                for i in range(row_num):
                    item = qtabel.item(i,col)
                    if item:
                        items.append(float(item.text()))
                if items:
                    index = items.index(min(items))
                    qtabel.item(index,col).setForeground(QtGui.QBrush(QtCore.Qt.blue))
            elif text == '删除':
                row = qtabel.currentItem().row()

                qtabel.removeRow(row)
            elif text == '复制':
                row = qtabel.currentRow()
                itemtext = ''
                if not qtabel.item(row,0):
                    return
                for i in range(19):
                    if qtabel.item(row,i):
                        item = qtabel.item(row,i).text()
                        itemtext += str(item)+'/'
                    else:
                        break
                app.clipboard().setText(itemtext)
    def dataFile(self):
        text = self.sender().text()
        if text == '选择文件':
            self.noisefile,filetype = QtWidgets.QFileDialog.getOpenFileName(None,'请选择wav文件',os.getcwd(),
                                                                      'Wav文件(*.wav)')
            wave = self.noisefile.split('/')[-1]
            self.noise_tool5.setText('已选择'+wave+'文件！')

        elif text == '单个wav统计':

            self.wavfile,filetype = QtWidgets.QFileDialog.getOpenFileName(None,'请选择wav文件',os.getcwd(),
                                                                      'Wav文件(*.wav)')
            wave = self.wavfile.split('/')[-1]
            self.wavelist = []
            self.data_tool9.setText('已选择'+wave+'文件！')

        else:
            waveTuple = QtWidgets.QFileDialog.getOpenFileNames(None,'请选择wav文件',os.getcwd(), 'Wav文件(*.wav)')
            self.wavelist = waveTuple[0]
            self.wavfile = ''
            for i in self.wavelist:
                self.data_tool9.append('已选择'+i+'文件！')

    def dataTabSub(self,url,type):
        window = self.data_view.currentSubWindow()

        data = analysisdata.DataAnalysis(url)
        aisle = data.aisle
        time = []
        if type == 0:
            time = data.getTimes()
        else:
            time = data.getFreqs()
        if not window:
            return [],[],[],[]
        qtabel = window.children()[-1]
        rownum = qtabel.rowCount()
        if aisle==1:
            rownum += 1
            qtabel.setRowCount(rownum)
            rownum = rownum-1
        else:
            rownum +=2
            qtabel.setRowCount(rownum)
            rownum = rownum-2
        t = qtabel.horizontalHeaderItem(1)
        if not t:
            qtabel.setColumnCount(19)
            dataitem = analysisdata.DataAnalysis.getTimeLabel()
            qtabel.setHorizontalHeaderLabels(dataitem)

        return time,rownum,qtabel,aisle

    def dataCopeItem(self,time,rownum,qtabel,type):
        if type == 0:
            for i in range(19):
                if i >2:
                    time[i] = round(time[i],4)
                    qtabel_item = QtWidgets.QTableWidgetItem()
                    qtabel_item.setData(QtCore.Qt.ItemDataRole.DisplayRole,float(time[i]))
                    qtabel_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    qtabel.setItem(rownum,i,qtabel_item)

                else:
                    qtabel_item = QtWidgets.QTableWidgetItem(str(time[i]))
                    qtabel_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    qtabel.setItem(rownum,i,qtabel_item)
            qtabel.setSortingEnabled(True)
        else:
            for i in range(13):
                    if i >2:
                        time[i] = round(time[i],4)
                        qtabel_item = QtWidgets.QTableWidgetItem()
                        qtabel_item.setData(QtCore.Qt.ItemDataRole.DisplayRole,float(time[i]))
                        qtabel_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        qtabel.setItem(rownum,i,qtabel_item)
                    else:
                        qtabel_item = QtWidgets.QTableWidgetItem(str(time[i]))
                        qtabel_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        qtabel.setItem(rownum,i,qtabel_item)
                    qtabel.setSortingEnabled(True)
    def dataCope(self):
        text = self.sender().text()
        if text == '时域统计':
            if self.wavfile:

                time,rownum,qtabel,aisle = self.dataTabSub(self.wavfile,0)
                #单元项
                if not time:
                    return
                if aisle == 1:
                    self.dataCopeItem(time,rownum,qtabel,0)

                else:
                    time_ = time[0]
                    self.dataCopeItem(time_,rownum,qtabel,0)

                    self.dataCopeItem(time[1],rownum+1,qtabel,0)

            elif self.wavelist:

                for wave in self.wavelist:
                    time,rownum,qtabel,aisle = self.dataTabSub(wave,0)
                #单元项
                    if not time:
                        return
                    if aisle == 1:
                        self.dataCopeItem(time,rownum,qtabel,0)

                    else:
                        time_ = time[0]
                        self.dataCopeItem(time_,rownum,qtabel,0)

                        self.dataCopeItem(time[1],rownum+1,qtabel,0)
            else:
                 QtWidgets.QMessageBox.information(self,'错误','未选择wav文件')
        elif text == '频域统计':
            if self.wavfile:

                time,rownum,qtabel,aisle = self.dataTabSub(self.wavfile,1)
                #单元项
                if not time:
                        return
                if aisle == 1:
                    self.dataCopeItem(time,rownum,qtabel,type)

                else:
                    time_ = time[0]
                    self.dataCopeItem(time_,rownum,qtabel,1)
                    self.dataCopeItem(time[1],rownum+1,qtabel,1)
            elif self.wavelist:

                for wave in self.wavelist:

                    #单元项
                    time,rownum,qtabel,aisle = self.dataTabSub(wave,1)
                #单元项
                    if not time:
                        return
                    if aisle == 1:
                        self.dataCopeItem(time,rownum,qtabel,type)

                    else:
                        time_ = time[0]
                        self.dataCopeItem(time_,rownum,qtabel,1)
                        self.dataCopeItem(time[1],rownum+1,qtabel,1)
            else:
                 QtWidgets.QMessageBox.information(self,'错误','未选择wav文件')

    def transFile(self):
        if not self.url:
            QtWidgets.QMessageBox.information(self,'信息提示','未选择文件')

        if '.' in self.url:
            self.trans_combobox.setCurrentIndex(1)
        else:
            self.trans_combobox.setCurrentIndex(2)
        transtype = self.trans_combobox.currentIndex()

        if self.sender().text()=='选择保存路径':
            self.savepath = QtWidgets.QFileDialog.getExistingDirectory(None,'请选择保存路径',os.getcwd())

        if self.sender().text() == '确认参数':

            self.waveaisle = self.rightWidget2_aisleline.text()
            self.samplenum = self.rightWidget2_sampleline.text()

            if transtype == 0:
                self.transinfor = QtWidgets.QMessageBox.information(self,'信息提示','未选择处理方式')
            else:
                if self.waveaisle and self.samplenum:

                    self.trans_text.setPlainText('选择的参数如下:\n处理方式:%s\n通道数%s\n采样率:%s\n保存路径%s'
                                            %(self.trans_combobox.currentText(),self.waveaisle,self.samplenum,self.savepath))


                else:

                    self.transinfor = QtWidgets.QMessageBox.information(self,'信息提示','未选择参数')


        if self.sender().text()=='开始转换':
            self.trans_text.setText('')
            if  transtype!=0 and self.waveaisle and self.samplenum:
                if transtype == 1:
                    if '.' in self.url:
                        predata.pcmcope(self.url,int(self.waveaisle),int(self.samplenum),self.savepath)
                        self.trans_text.setText(self.url+'转换完成！')
                    else:
                        QtWidgets.QMessageBox.information(self,'信息提示','模式不匹配')
                else:
                    if '.' in self.url:
                        QtWidgets.QMessageBox.information(self,'信息提示','模式不匹配')
                    else:
                        pcmlist = os.listdir(self.url)
                        k = 0
                        for p in pcmlist:
                            if p[-4:]=='.pcm':
                                url = self.url
                                url += '/'+p
                                predata.pcmcope(url,int(self.waveaisle),int(self.samplenum),self.savepath)
                                self.trans_text.append(url+'转换完成！')
                                k+=1
                        self.trans_text.append('全部转换完成，共完成了%s项！'%(k))
            else:
                self.transinfor = QtWidgets.QMessageBox.information(self,'信息提示','未确认参数')

    def singleFile(self):
        self.url,filetype = QtWidgets.QFileDialog.getOpenFileName(None,'选取单个文件',os.getcwd()
                                                             ,'Pcm File(*.pcm)')
        u = self.url.split('/')[-1]
        self.trans_text.setText('  选择的文件是:%s。等待后续处理...'%(u))
    def batchFile(self):
        self.url = QtWidgets.QFileDialog.getExistingDirectory(None,'选取待处理文件夹',os.getcwd())
        self.trans_text.setText('  选择的文件夹是:%s。等待后续处理...'%(self.url))

    def select_Widget(self):


        if self.sender().text()=='首页':

            self.rightWidget.setCurrentIndex(1)
        if self.sender().text()=='文件转换':
            self.rightWidget.setCurrentIndex(2)
        if self.sender().text()=='波形分析':
            self.rightWidget.setCurrentIndex(3)
        if self.sender().text()=='降噪处理':
            self.rightWidget.setCurrentIndex(4)
        if self.sender().text()=='模型降噪':
            self.rightWidget.setCurrentIndex(6)
        if self.sender().text()=='已存数据':
            self.rightWidget.setCurrentIndex(5)
            self.rightWidget5.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

            #读入本地json数据
            if not os.path.exists('./logging.json'):
                data = {}
                with open('./logging.json','w') as f:
                    json.dump(data,f)

            with open('./logging.json','r') as f:
                origin_data = json.load(f)
            if not origin_data:
                origin_data['头'] =  []
                origin_data['data'] = []
            json_len = len(origin_data['头'])
            self.rightWidget5.setRowCount(json_len)

            if not  json_len ==0 :
                for i in range(json_len):
                    self.rightWidget5.setRowHeight(i,40)
                    file = origin_data['data'][i][-1]
                    file = file.split('+')
                    self.saveitem(i,file[1],file[2])
                    btn = QtWidgets.QPushButton('打开')
                    btn.setFixedWidth(100)
                    btn.setFixedHeight(35)
                    btn.setStyleSheet('margin-top:5px;margin-left:20px;')
                    self.rightWidget5.setCellWidget(i,3,btn)
                    btn.clicked.connect(self.opensave)

            noiseviews = self.noise_view.subWindowList()
            noise_len = len(noiseviews)
            dataviews = self.data_view.subWindowList()
            data_len = len(dataviews)

            ctime = QtCore.QDateTime()
            ctime = ctime.currentDateTime()
            ctime = ctime.toString('yyyy-MM-dd hh:mm:ss dddd')
            dataview0 = dataviews[0].children()[-1]

            if not data_len == 0 :

                file = ''
                if self.wavfile:
                    file = self.wavfile
                else:
                    file = self.wavelist

                save_row = self.rightWidget5.rowCount()
                self.rightWidget5.setRowCount(save_row+1)

                self.saveitem(save_row,ctime,'波形分析')
            if not noise_len == 0 :

                save_row = self.rightWidget5.rowCount()
                self.rightWidget5.setRowCount(save_row+1)
                self.saveitem(save_row,ctime,'降噪处理')

    def opensave(self):
        x = self.sender().geometry().x()
        y = self.sender().geometry().y()
        index = self.rightWidget5.indexAt(QtCore.QPoint(x,y))
        row = index.row()
        with open('./logging.json','r') as f:
            load_data = json.load(f)
        pages_lists = load_data['data2'][row]
        pages_num = len(pages_lists)
        k=0
        item_type = self.rightWidget5.item(row,2).text()

        #不同页面打开
        if item_type == '波形分析':
            self.rightWidget.setCurrentIndex(3)
            pages_num = pages_num-1
            for i in range(pages_num):
                page = pages_lists[i]
                self.dataViewAdd()
                if len(page) == 1:
                    return
                else:

                    #不同文件打开
                    file_names = []
                    files = page.split('+')[:-1]

                    file_len = len(files)

                    for j in range(file_len):
                        file = files[j]
                        file_split = file.split('!')
                        aisle = int(file_split[-1])

                        data = []
                        if aisle == 2 and k==0:
                            data.append(file_split[0])
                            data.append(file_split[1])
                            file_names.append(data)
                            k=1

                        elif aisle == 2 and k==1:
                            k=0
                            continue
                        else:

                            data.append(file_split[0])
                            data.append(file_split[1])
                            file_names.append(data)
                    #打开不同数据表
                    url_len = len(file_names)
                    for k in range(url_len):
                        url = file_names[k][0]
                        type = file_names[k][1]
                        if '时域' in type:
                            time,rownum,qtabel,aisle = self.dataTabSub(url,0)
                            if aisle == 1:
                                self.dataCopeItem(time,rownum,qtabel,0)

                            else:
                                time_ = time[0]
                                self.dataCopeItem(time_,rownum,qtabel,0)

                                self.dataCopeItem(time[1],rownum+1,qtabel,0)
                        else:
                            time,rownum,qtabel,aisle = self.dataTabSub(url,1)
                            #单元项
                            if aisle == 1:
                                self.dataCopeItem(time,rownum,qtabel,type)

                            else:
                                time_ = time[0]
                                self.dataCopeItem(time_,rownum,qtabel,1)
                                self.dataCopeItem(time[1],rownum+1,qtabel,1)
                    v = pages_num-1
                    if  i == v:

                        break

        else:
            self.rightWidget.setCurrentIndex(4)
            url = pages_lists[-2]
            pages_lists = pages_lists[0:-2]

            self.noisefile = url
            pages_num = len(pages_lists)
            view_num = len(self.noise_view.subWindowList())

            for i in range(pages_num):
                page = pages_lists[i]
                page_type = page[-1]

                if page_type=='1':
                    self.fllwave()

                    noiseviews = self.noise_view.subWindowList()

                    view = noiseviews[i+view_num ]
                    tab_view = view.children()[-1]
                    stack = tab_view.children()[0]
                    line1 = stack.children()[3].findChildren(QtWidgets.QLineEdit)
                    line2 = stack.children()[1].findChildren(QtWidgets.QLineEdit)
                    line3 = stack.children()[0].findChildren(QtWidgets.QLineEdit)


                    line1[0].setText(page[0])
                    line1[1].setText(page[1])
                    line2[0].setText(page[2])
                    line3[0].setText(page[3])

                elif page_type=='2':
                    self.wavereduce()
                    noiseviews = self.noise_view.subWindowList()
                    view = noiseviews[i+view_num ]
                    line = view.findChild(QtWidgets.QLineEdit)
                    line.setText(page[0])
                else:

                    self.karmanwave()
                    noiseviews = self.noise_view.subWindowList()
                    view = noiseviews[i+view_num ]
                    lines = view.findChildren(QtWidgets.QLineEdit)
                    lines[0].setText(page[0])
                    lines[1].setText(page[1])
    def saveitem(self,row,time,type):
        item = QtWidgets.QTableWidgetItem(f'文件{row+1}')
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.rightWidget5.setItem(row,0,item)

        item = QtWidgets.QTableWidgetItem(str(time))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.rightWidget5.setItem(row,1,item)

        item = QtWidgets.QTableWidgetItem(type)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.rightWidget5.setItem(row,2,item)



    def saveMenu(self,pos):
        menu = QtWidgets.QMenu()
        menu.addAction('保存')
        menu.addAction('删除')
        p = self.rightWidget5.mapToGlobal(pos)
        action = menu.exec(p)
        if not action:
            return
        text = action.text()
        current_row = self.rightWidget5.currentRow()
        item_type = self.rightWidget5.item(current_row,2).text()

        ctime = QtCore.QDateTime()
        ctime = ctime.currentDateTime()
        ctime = ctime.toString('yyyy-MM-dd hh:mm:ss dddd')

        if text == '保存' and item_type=='波形分析':

            dataviews = self.data_view.subWindowList()
            data_len = len(dataviews)
            save_row = self.rightWidget5.rowCount()-1
            data_list = []
            #每一页的数据
            for i in range(data_len):
                d = dataviews[i]
                d = d.children()[-1]
                row = d.rowCount()

                data = ''
                if row == 0:
                    continue
                for r in range(row):
                    data += d.item(r,0).text()+'!'+d.item(r,1).text()+'!'+d.item(r,3).text()+'+'
                data_list.append(data)


            data_list.append(f'文件{save_row+1}'+'+'+ctime+'+'+'波形分析')

            with open('./logging.json','r') as f:
                json_data = json.load(f)
            json_len = len(json_data)
            if not json_len:
                json_data['头'] =  []
                json_data['头'].append(0)
                json_data['data2'] = []
                json_data['data2'].append(data_list)

            else:
                json_data['头'].append(len(json_data['头']))
                json_data['data2'].append(data_list)
            with open("./logging.json","w") as f:
                json.dump(json_data,f)

        elif text == '保存' and item_type=='降噪处理':
            noiseviews = self.noise_view.subWindowList()
            noise_len = len(noiseviews)


            noise_file = []
            for i in range(noise_len):
                noise_data = []
                noise_page = noiseviews[i].children()[-1]
                title = noise_page.windowTitle()
                if title == '傅立叶滤波':
                    lines = noise_page.findChildren(QtWidgets.QLineEdit)
                    noise_data.append(lines[0].text())
                    noise_data.append(lines[1].text())
                    noise_data.append(lines[2].text())
                    noise_data.append(lines[3].text())
                    noise_data.append('1')
                elif title == '谱减法滤波':
                    lines = noise_page.findChild(QtWidgets.QLineEdit)
                    noise_data.append(lines.text())
                    noise_data.append('2')
                else:
                    lines = noise_page.findChildren(QtWidgets.QLineEdit)
                    noise_data.append(lines[0].text())
                    noise_data.append(lines[1].text())
                    noise_data.append('3')

                noise_file.append(noise_data)
            noise_file.append(self.noisefile)
            noise_file.append(f'文件{current_row}'+'+'+ctime+'+'+'降噪处理')
            with open('./logging.json','r') as f:
                json_data = json.load(f)
                json_len = len(json_data)
            if not json_len:
                json_data['头'] =  []
                json_data['头'].append(0)
                json_data['data2'] = []
                json_data['data2'].append(noise_file)

            else:
                json_data['头'].append(len(json_data['头']))
                json_data['data2'].append(noise_file)
            with open("./logging.json","w") as f:
                json.dump(json_data,f)

        elif text == '删除':
            row = self.rightWidget5.currentRow()
            row_num = self.rightWidget5.rowCount()
            if row>=row_num-2:
                self.rightWidget5.removeRow(row)
                return
            self.rightWidget5.removeRow(row)

            #删除
            with open('./logging.json','r') as f:
                json_data = json.load(f)
            json_data['头'].pop(row)
            json_data['data2'].pop(row)
            with open("./logging.json","w") as f:
                json.dump(json_data,f)

            # noiseview = noiseMdi.currentSubWindow()


            #
            # index = dataview.item(0,1)
            # if index:
            #     print(dataview.item(0,0),dataview.item(0,1))
            # if noiseview:
            #     noiseview = noiseMdi.currentSubWindow().children()[-1]




if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    win = SonaWindow()

    win.show()
    sys.exit(app.exec_())
