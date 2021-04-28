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
from listener_logfile import listener_logfile_process
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
                    '%(message)s')
                self.poped.emit(str(formatter.format(data)))

class MainWindow(QMainWindow, window):
    def __init__(self):
        super().__init__()
        self.viewer_queue = Queue(-1)
        self.listener = Process(
            target=listener_process, args=(self.viewer_queue, ))
        self.listener.start()

        self.file_queue = Queue(-1)
        self.listener_logfile = Process(
            target=listener_logfile_process, args=(self.file_queue, ))
        self.listener_logfile.start()

        self.root_configurer(self.viewer_queue)

        self.setupUi(self)
        self.plainTextEdit.setReadOnly(True)
        self.consumer = Consumer(self.viewer_queue)
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
        if self.lineEdit.text() is "":
            logging.warning(f"Please enter the content your looking for")
            return False
        if self.lineEdit_2.text() is "":
            logging.warning(f"Please enter the number of images to crawl")
            return False
        self.imagecrawler = ImageCrawler()
        p = Process(name="crawler",
            target=self.imagecrawler.crawl, args=(self.lineEdit.text(), self.viewer_queue, self.file_queue, self.lineEdit_2.text(), ))
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