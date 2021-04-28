import logging
from logging import handlers
from time import sleep
from datetime import datetime
import os


def listener_configurer():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(message)s')
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)


def listener_process(queue):
    listener_configurer()
    while True:
        while not queue.empty():
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        sleep(1)