import logging
from logging import handlers
from time import sleep
from datetime import datetime


def listener_configurer():
    root = logging.getLogger()
    file_handler = handlers.RotatingFileHandler(
        '.\\log\\' + datetime.now().format('%y%m%d%H%M%S') + '.log', 'a', 50000000000, 5)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    root.addHandler(console_handler)
    root.setLevel(logging.DEBUG)


def listener_process(queue):
    listener_configurer()
    while True:
        while not queue.empty():
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        sleep(1)