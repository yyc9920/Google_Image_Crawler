from multiprocessing import Process, Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import wget
import subprocess
import logging
from googleimagecrawler import ImageCrawler
from PyQt5 import QtCore, uic, QtGui, QtWidgets
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
from logging import handlers

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
import sys
from listener import listener_process
from PyQt5.Qt import QIntValidator

window = uic.loadUiType(".\\gic.ui")[0]

logger = logging.getLogger(__name__)

# logging.LogRecord()
class Consumer(QThread):
    poped = Signal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                formatter = logging.Formatter(
                    '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
                self.poped.emit(str(formatter.format(data)))

class MainWindow(QMainWindow, window):
    def __init__(self):
        super().__init__()
        self.queue = Queue(-1)
        self.listener = Process(
            target=listener_process, args=(self.queue, ))
        self.listener.start()

        self.root_configurer(self.queue)

        self.setupUi(self)
        self.plainTextEdit.setReadOnly(True)
        self.consumer = Consumer(self.queue)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        self.lineEdit_2.setValidator(QIntValidator())
        self.pushButton.clicked.connect(self.crawling)

    def root_configurer(self, queue):
        h = handlers.QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)

    def crawling(self):
        content = self.lineEdit.text()
        self.imagecrawler = ImageCrawler()
        print(content)
        p = Process(name="crawler",
            target=self.imagecrawler.crawl, args=(content, self.queue, self.lineEdit_2.text(), ))
        p.start()

    @Slot(str)
    def print_data(self, data):
        self.plainTextEdit.appendPlainText(data)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()