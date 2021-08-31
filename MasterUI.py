#-*- codeing = utf-8 -*-
#@Time :  
#@Author: Mianbao
#@File : MasterUI.py
#@Software : PyCharm
import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import ico


class masterUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.master_ui()
    def master_ui(self):
        self.setFixedSize(1200, 400)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_2 = QtWidgets.QPushButton("Where Is My Mind ? ")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("功能尚未开发")
        self.left_label_3.setObjectName('left_label')
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='black'), "影片搜索")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='black'), "自动粘贴到剪贴板")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='black'), "字幕搜索")
        self.left_button_3.setObjectName('left_button')

        # self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_2, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)

        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

        self.left_widget.setStyleSheet('''
                   QPushButton{border:none;color:black;}
                   QPushButton#left_label{
                       border:none;
                       color:#232C51;
                       border-bottom:1px solid white;
                       font-size:18px;
                       font-weight:700;
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                   }
                   QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
               ''')
        self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                        color:#232C51;
                        background:white;
                        border-top:1px solid darkGray;
                        border-bottom:1px solid darkGray;
                        border-right:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                    QLabel#right_lable{
                        border:none;
                        font-size:16px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                ''')
        self.setWindowOpacity(0.8)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        self.setWindowIcon(QIcon(':/Myico.ico'))
        # self.setWindowIcon(QIcon(r'D:\爬虫\GetMovie\NewProject\Myico.ico'))
        self.setWindowTitle("Where is the movie")
