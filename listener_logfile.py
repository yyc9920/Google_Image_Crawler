import logging
from logging import handlers
from time import sleep
from datetime import datetime
import os


def listener_configurer():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    try:
        os.mkdir('log')
    except Exception as e:
        # print(e)
        print("\nlog Folder Already Exists\n")
    file_handler = handlers.RotatingFileHandler(
        '.\\log\\' + datetime.now().strftime('%y%m%d%H%M%S') + '.log', 'a', 50000000, 5)
    formatter = logging.Formatter(
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)


def listener_logfile_process(queue):
    listener_configurer()
    while True:
        while not queue.empty():
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        sleep(1)