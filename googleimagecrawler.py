from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import wget
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from urllib3.connectionpool import log
LOGGER.setLevel(logging.WARNING)
log.setLevel(logging.WARNING)

from PyQt5 import QtCore, QtGui, QtWidgets
Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

logger = logging.getLogger(__name__)

class ImageCrawler:
    def __init__(self):
        super().__init__()

    def worker_configurer(self, queue):
        h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
        root = logging.getLogger()
        root.addHandler(h)
        # send all messages, for demo; no other level or filter logic applied.
        root.setLevel(logging.DEBUG)

    def scroll_down(self, driver, last_height):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                return 0
        last_height = new_height
    
    # @Slot()
    def crawl(self, content, queue, queue_logfile, number):
        self.worker_configurer(queue)
        self.worker_configurer(queue_logfile)
        logging.info(f"Search " + content + " in Google for Image Crawling")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(".\\chromedriver.exe", options=options)
        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
        elem = driver.find_element_by_name("q")
        elem.send_keys(content)
        elem.send_keys(Keys.RETURN)
        last_height = driver.execute_script("return document.body.scrollHeight")

        try:
            os.makedirs('.\\images\\' + content)
        except Exception as e:
            print("The Images of " + content + " has been already crawled and downlaoded")
            logging.warning(f"The Images of " + content + " has been already crawled and downlaoded")
            logging.warning(f"Please search for other contents or erase the " + content + " folder and retry crawling")
            driver.close()
            return False
        images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        while (len(images) < int(number)):
            self.scroll_down(driver, last_height)
            images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        count = 1
        for i, image in enumerate(images):
            if (int(number) < i):
                break
            logging.info(f"Download Image of " + content + " no. " + str(count))
            try:
                image.click()
                time.sleep(5)
                imgUrl = driver.find_element_by_xpath(
                    '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
                wget.download(imgUrl, '.\\images\\' + content + "\\" + str(count) + ".jpg")
                time.sleep(3)
                count = count + 1
            except:
                pass
        driver.close()
        logging.info(f"Crawling " + content + " is Done!!")

if __name__=='__main__':
    crawler = ImageCrawler()
    crawler.crawl("있지 예지")