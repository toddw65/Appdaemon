import appdaemon.plugins.hass.hassapi as hass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from cairosvg import svg2png
import datetime
import time
from pyvirtualdisplay import Display


#
# Scrape data from MyFerrellGas.com
# Update sensor in HASS
# Create tank image based on tank percentage
#

class MyFerrellGas(hass.Hass):
    def initialize(self):
        self.log("MyFerrellGas loaded")
        runtime = datetime.time(2, 30, 0)
        self.run_daily(self.do_scrape, runtime)

    def do_scrape(self, event_name):
        try:
            login_name = self.args["login_name"]
            login_pass = self.args["login_pass"]
            site_url = self.args["site_url"]
            img_save_path = self.args["img_save_path"]
                        
            display = Display(visible=0, size=(800, 600))
            display.start()
            browser = webdriver.Firefox()
            self.log("Browser created.")

            browser.implicitly_wait(30)
            browser.get(site_url)
            self.log("Getting website %s." % site_url)
            username = browser.find_element_by_id("input_0")
            self.log("Found username field.")
            password = browser.find_element_by_id("input_1")
            self.log("Found password field.")
            submit = browser.find_element_by_id("btnLogin")
            self.log("Found submit button.")
            username.send_keys(login_name)
            self.log("Sent username %s." % login_name)
            password.send_keys(login_pass)
            self.log("Sent password %s." % login_pass)
            submit.click()
            browser.implicitly_wait(60)
            self.log(browser.find_element_by_class_name("tank-pct").get_attribute("innerHTML"))
            pct = browser.find_element_by_class_name("tank-pct").get_attribute("innerHTML").replace("%","")
            self.log(pct+"%")
            svg_part_1 = """<svg xmlns="http://www.w3.org/2000/svg" class="tank" viewBox="0 0 200 125">
            <path
                class="tankpath"
                d="M97.624 4.98c-13.16 0-23.755 10.262-23.755 23.008h-21.379c-26.32 0-47.51 20.523-47.51 46.016s21.189 46.016 47.51 46.016h95.02c26.32 0 47.51-20.523 47.51-46.016s-21.189-46.016-47.51-46.016h-21.379c0-12.746-10.595-23.008-23.755-23.008h-4.751z"
                id="path4610"
                style="stroke:#bafcfb;stroke-opacity:1;fill:#0d7ba4;fill-opacity:1" />"""
            if int(pct) >= 75:
                svg_part_2 = """<path class="tank-fill-80 " d="M 15.505,44.973 184.805,45 c 22.28241,30.147861 5.54653,71.45116 -34.28348,74.79999 l -101.21636,0.2852 C 1.3631941,114.55969 -3.5255293,64.489954 15.506,44.972 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 65 and int(pct) < 75:
                svg_part_2 = """<path class="tank-fill-70 " d="m 12.629,53.413 177.35876,-0.011 c 15.39061,29.063593 -5.37286,64.63153 -40.23765,66.49429 l -99.097722,0.0926 C 15.827493,118.94423 -5.6706678,82.216778 9.9325439,53.412 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 55 and int(pct) < 65:
                svg_part_2 = """<path class="tank-fill-60 tank-fill" d="m 193.64863,62.992 c 5.94794,25.706756 -10.02215,54.65902 -45.03407,57.07382 l -95.991981,-0.0278 C 13.207023,118.4254 0.1674334,83.2465 6.3659784,63.018038 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 45 and int(pct) < 55:
                print(int(pct))
                svg_part_2 = """<path class="tank-fill-50 " d="m 195.0035,72.006962 c 0.81316,24.467867 -16.32249,46.210268 -46.73481,48.045218 l -97.27547,0.002 C 18.478405,117.63067 4.3676285,93.353155 5.0073944,72.006 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 35 and int(pct) < 45:
                svg_part_2 = """<path class="tank-fill-40 " d="m 194.47138,81.018076 c -3.50791,22.329874 -23.13371,38.913544 -47.10875,39.023664 l -96.016052,-0.0157 C 26.224568,119.8284 8.2369447,100.00246 5.532886,80.98 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 25 and int(pct) < 35:
                svg_part_2 = """<path class="tank-fill-30 " d="m 192.07627,89.983924 c -6.91925,17.768676 -23.43993,29.707806 -44.66549,30.033746 l -95.498266,0.003 C 31.529321,119.69798 14.693792,107.61371 7.9073832,89.989976 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) >= 15 and int(pct) < 25:
                svg_part_2 = """<path class="tank-fill-20 " d="m 187.43954,99.026048 c -6.40291,10.147762 -20.35578,20.968682 -39.68157,20.992082 l -96.411392,-0.004 C 38.907512,120.14951 22.607557,114.15437 12.627,98.982 Z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            elif int(pct) < 15:
                svg_part_2 = """<path class="tank-fill-10 " d="m 179.56145,108.01008 c -9.99212,8.26245 -18.08352,11.23693 -31.75342,12.06777 l -96.36515,-0.0398 c -11.127238,0.2693 -23.04633,-5.29912 -31.096147,-12.05319 z" style="display:inline;fill:#0056a4;fill-opacity:1;stroke-width:0.99000001" ></path>"""
            svg_part_3 =  """<text class="tank-pct" alignment-baseline="baseline" x="111.86662" y="77.073944" id="text4608" style="font-size:37.13151169px;text-anchor:middle;display:inline;fill:#00b7ea;fill-opacity:1;stroke-width:3.09429264" transform="scale(0.89216954,1.1208632)">"""
            svg_part_4= "%</text></svg>"
            svg_tank = svg_part_1+svg_part_2+svg_part_3+pct+svg_part_4	 
            svg2png(bytestring=svg_tank,write_to = img_save_path)
        finally:
            browser.quit()
            display.sendstop()