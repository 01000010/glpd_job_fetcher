###############################################################################
### Libraries and imports #####################################################
###############################################################################

import os
import time
from selenium.webdriver import Chrome 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

###############################################################################
### Classes ###################################################################
###############################################################################

class cc: # Console color
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class msg: # Console message
    @staticmethod
    def warning(string, nl = True, bold = False, underline = False):
        _str = cc.WARNING
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str) if nl == True else print(_str, end = " ")

    @staticmethod
    def ok(string, nl = True, bold = False, underline = False):
        _str = cc.OKGREEN
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str)

    @staticmethod
    def okb(string, nl = True, bold = False, underline = False):
        _str = cc.OKBLUE
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str) if nl == True else print(_str, end = " ")

    @staticmethod
    def fail(string, nl = True, bold = False, underline = False):
        _str = cc.FAIL
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str) if nl == True else print(_str, end = " ")

    @staticmethod
    def header(string, nl = True, bold = False, underline = False):
        _str = cc.HEADER
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str) if nl == True else print(_str, end = " ")
    
    @staticmethod
    def norm(string, nl = True, bold = False, underline = False):
        _str = ""
        if(bold):
            _str += cc.BOLD
        if(underline):
            _str += cc.UNDERLINE
        _str += string + cc.ENDC
        print(_str) if nl == True else print(_str, end=" ")

###############################################################################
### Functions #################################################################
###############################################################################

def wait_page_load(web_driver, elem_id):
    msg.norm("Waiting for page load...")
    result = WebDriverWait(web_driver, 30).until(
        lambda x: x.find_element_by_id(elem_id)
    )
    return result

def save_page_html(web_driver, file_name, dir_path = "page/"):
    full_name = dir_path + file_name
    os.makedirs(os.path.dirname(full_name), exist_ok=True)
    msg.warning(str.format("Saving initial html data into: {0}{1}",
        dir_path, file_name))
    try:
        with open(str.format("{0}{1}", dir_path, file_name), "w") as f:
            f.write(web_driver.page_source)
            f.close()
        msg.ok("File saved!!!!", bold=True, underline=True)
    except:
        msg.fail("Couldn't save File!!!!", bold=True, underline=True)
    return

def get_credentials(file_name):
    with open(file_name, "r") as f:
        contents = f.readlines()
        f.close()
        #      --- URL ---         --- User ---       --- Password ---        
    return contents[0].strip(), contents[1].strip(), contents[2].strip()

###############################################################################
### Main script ###############################################################
###############################################################################

c_file = "credentials.txt"
try:
    url, usr, psw = get_credentials(c_file)
except:
    msg.fail(str.format("Could not read file {0}", c_file), 
        bold=True, underline=True)
    exit(1)
# initialize a new session of chrome and log in into the account
msg.header("Initializing Chrome...", bold=True)
driver = Chrome()
driver.get(url)
msg.warning("Accessing web page...")
button_login = driver.find_element_by_id("loginwithemail-button")
button_login.click()
msg.warning("Logging-in...")
box_usr = driver.find_element_by_id("Email")
box_usr.send_keys(usr)
box_usr.send_keys('\ue007')
box_psw = driver.find_element_by_id("Password")
box_psw.send_keys(psw)
box_psw.send_keys('\ue007')
msg.okb("Logged-in!!!")
# wait for the web page to load by targetting an id
table_view = "tableview-1044"
wait_page_load(driver, table_view)
save_page_html(driver, "page_code_wo_jobs.html")

# main loop for the job hunt
while(True): # while no job is confirmed
    while(True): # while no job found on the list
        msg.norm("Refreshing page...")
        driver.refresh()
        wait_page_load(driver, table_view)
        # get table of available jobs
        msg.norm("Looking for jobs...")
        table_jobs = driver.find_elements_by_xpath(
            '//*[@class="x-grid-item-container"]')
        num_jobs = len(table_jobs)
        msg.norm(str.format("{0} jobs found.", num_jobs))
        if(num_jobs > 0):
            msg.okb("Jobs found! Saving html for analysis...")
            save_page_html(driver, "page_code_w_jobs.html")
            break
    msg.ok("Fetching the first job of the list...", bold=True)
    # TODO
