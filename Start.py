#-*- codeing = utf-8 -*-
#@Time :  
#@Author: Mianbao
#@File : Start.py
#@Software : PyCharm

import os
from threading import Thread
import qtawesome
from PyQt5 import QtGui,QtWidgets
import sys
from PyQt5.QtWidgets import QMessageBox
from MasterUI import masterUI
from DBManger import sqlite_db
import pyperclip
import getSubtitle
from subDBManger import subtitle_db



class MainUi(masterUI):
    __instance = None
    def __init__(self):
        super().__init__()
        self.sub = subtitle_db()
        self.sq = sqlite_db()
        self.init_ui()

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MainUi, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def init_ui(self):
        print("被创建")
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入电影名称，回车进行搜索")
        self.right_bar_widget_search_input.returnPressed.connect(self.do_search)
        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        self.right_bar_widget_search_input.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')
        self.view = QtWidgets.QTableView(showGrid=False)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["电影名称","画质","资源名称","大小", "磁力链接"])
        self.view.setModel(self.model)
        self.view.clicked.connect(self.test)

        self.view2 = QtWidgets.QTableView(showGrid=False)
        self.view2.horizontalHeader().setStretchLastSection(True)
        self.model2 = QtGui.QStandardItemModel()
        # self.model2.isWidgetType()
        self.model2.setHorizontalHeaderLabels(["字幕名称","下载地址"])
        self.view2.setModel(self.model2)
        self.view2.clicked.connect(self.test2)

        self.right_bar_layout.addWidget(self.view, 1, 0, 1, 10)
        self.right_bar_layout.addWidget(self.view2, 2, 0, 30, 10)

    def do_search2(self):
        print("sousuo")
        def loop():
            for i in range(0,10):
                item_3 = QtGui.QStandardItem(str(i))
                item_4 = QtGui.QStandardItem(i)
                self.model.appendRow([item_3, item_4])
                print(i)
        def threadFunc():

            for i in range(20,30):
                item_3 = QtGui.QStandardItem(str(i))
                item_4 = QtGui.QStandardItem(i)
                self.model2.appendRow([item_3, item_4])
                print(i)

        thread = Thread(target=threadFunc)
        thread.start()
        pass
    def do_search(self):
        self.model.clear()
        self.model2.clear()
        self.model.setHorizontalHeaderLabels(["电影名称", "画质", "资源名称", "大小", "磁力链接"])
        self.model2.setHorizontalHeaderLabels(["字幕名称", "下载地址"])
        word = self.right_bar_widget_search_input.text()
        self.query = {}
        def threadFunc():
            self.query = self.sq.selectResourceByMovieid(word).fetchall()
            for item in self.query:
                item_3 = QtGui.QStandardItem(item[1])
                item_4 = QtGui.QStandardItem(item[3])
                item_5 = QtGui.QStandardItem(item[2])
                item_6 = QtGui.QStandardItem(item[4])
                item_7 = QtGui.QStandardItem(item[5])
                # print(item[0])
                # print(item[1])
                # print('=========',type([item_3, item_7]))
                self.model.appendRow([item_3, item_4, item_5, item_6, item_7])
            getSubtitle.do(word)
            self.query2 = self.sub.selectMovie(word).fetchall()
            for item in self.query2:
                item_1 = QtGui.QStandardItem(item[0])
                item_2 = QtGui.QStandardItem(item[1])
                # print(item[0])
                # print(item[1])
                # print('=========', type([item_1, item_2]))
                self.model2.appendRow([item_1, item_2])

        thread = Thread(target=threadFunc)
        thread.start()
        QMessageBox.information(self, '提示信息', '正在查找：' + word + '... ')

    def test(self):
        key = self.view.selectedIndexes()[0].data()
        value = pyperclip.copy(key)
        print(value)

    def test2(self):
        key = self.view2.selectedIndexes()[0].data()
        value = pyperclip.copy(key)
        print(value)

    def clearn(self):
        self.sub.cur.close()

        self.sub.close_connect()
        try:
            os.remove("subtitle.sqlite")
        except Exception as e :
            print(e)
            self.sub = subtitle_db()
            reply = QtWidgets.QMessageBox.question(self, 'bibo', '请等待搜索结束',
                                                   QtWidgets.QMessageBox.Yes)

    def printToGui(self, fb, text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    # def closeEvent(self, event):
    #     # self.sub.close_connect()
    #     # os.remove("subtitle.sqlite")
    #     reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？',
    #                                            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def main(self):
    #     self.app = QtWidgets.QApplication(sys.argv)
    #     self.window().show()
    #     sys.exit(self.app.exec_())

def main():
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QIcon())
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

# def do_search():
#     print("sousuo")
#     pass

# def copyText():
#     # 变量
#     key = '双峰'
#     # 拷贝变量到剪切板
#     value = pyperclip.copy(key)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QIcon())
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
    # main()
#     MainUi().main()
