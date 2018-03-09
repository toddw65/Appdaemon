import appdaemon.plugins.hass.hassapi as hass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
import datetime
import time
from pyvirtualdisplay import Display
import pymysql

class ScrapeDishChannels(hass.Hass):
    def initialize(self):
        self.log("ScrapeDishChannels loaded.")
        runtime = datetime.time(2, 15, 0)
        self.run_daily(self.scrape_channels, runtime)

    def scrape_channels(self, event_name):  
        host_ip = self.args["host_ip"]
        db_user = self.args["db_user"]
        db_pass = self.args["db_pass"]
        db_name = self.args["db_name"]
        scrape_url = self.args["scrape_url"]
        
        conn = pymysql.connect(host = host_ip, user = db_user, passwd = db_pass, db = db_name, charset='utf8')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS dish_channels")
        sql = "CREATE TABLE dish_channels (channel_number smallint(6), channel_abbrev varchar(256),  channel_name varchar(255))"
        c.execute(sql)
        site_url = scrape_url
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        self.log("Browser created.")
        browser.get(site_url)
        self.log("Getting website %s." % site_url)
        table = browser.find_element_by_xpath("//table[2]")

        for row in table.find_elements_by_xpath(".//tr"):
            if len(row.find_element_by_xpath(".//td[1]").text.strip()) >= 1 and len(row.find_element_by_xpath(".//td[1]").text.strip()) < 9 and row.find_element_by_xpath(".//td[1]").text.find("-") < 0:
                channel_number = row.find_element_by_xpath(".//td[1]").text.strip()
                channel_abbrev = row.find_element_by_xpath(".//td[2]").text.strip()
                channel_name = row.find_element_by_xpath(".//td[3]").text.strip()
                c.execute("""INSERT INTO dish_channels VALUES (%s,%s,%s)""",(channel_number, channel_abbrev, channel_name))
                conn.commit()

        conn.close()
        browser.quit()
        display.sendstop()