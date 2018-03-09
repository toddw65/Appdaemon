import appdaemon.plugins.hass.hassapi as hass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
import time
from pyvirtualdisplay import Display
import pymysql

class TestTriggerTable(hass.Hass):
    def initialize(self):
        self.listen_state(self.update_now,"input_boolean.script_trigger")

    def update_now(self, entity, attribute, old, new, kwargs):  
        conn = pymysql.connect(host = "192.168.0.100", user = "hass", passwd = "sierra91", db = "hass_db", charset='utf8')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS dish_channels")
        sql = "CREATE TABLE dish_channels (channel_number smallint(6), channel_abbrev varchar(256),  channel_name varchar(255))"
        c.execute(sql)
        site_url = "http://uplink.jameslong.name/channels.html"
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
                #self.log(channel_number + " - " + channel_abbrev + " - " + channel_name)
                c.execute("""INSERT INTO dish_channels VALUES (%s,%s,%s)""",(channel_number, channel_abbrev, channel_name))
                conn.commit()
        #conn.rollback()        
        #self.log("Database error occurred!")
        conn.close()
        browser.quit()
        display.sendstop()