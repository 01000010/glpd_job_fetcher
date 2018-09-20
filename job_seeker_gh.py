# https://gl-tptprod1.transperfect.com/PD/login
# usr = user
# psw = password

###############################################################################
### Libraries and imports #####################################################
###############################################################################

import time
from selenium.webdriver import Chrome 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

###############################################################################
### Functions #################################################################
###############################################################################

def wait_page_load(web_driver, elem_id):
    result = WebDriverWait(web_driver, 30).until(
        lambda x: x.find_element_by_id(elem_id)
    )
    return result

###############################################################################
### Main script ###############################################################
###############################################################################

usr = ""
psw = "" 
# initialize a new session of chrome and log in into the account
print("Initializing Chrome...")
driver = Chrome()
driver.get("https://gl-tptprod1.transperfect.com/PD")
button_login = driver.find_element_by_id("loginwithemail-button")
button_login.click()
print("Logging-in...")
box_usr = driver.find_element_by_id("Email")
box_usr.send_keys(usr)
box_usr.send_keys('\ue007')
box_psw = driver.find_element_by_id("Password")
box_psw.send_keys(psw)
box_psw.send_keys('\ue007')
print("Logged-in!")
# wait for the web page to load by targetting an id
table_view = "tableview-1044"
wait_page_load(driver, table_view)

# main loop for the job hunt
while(True): # while no job is confirmed
    while(True): # while no job found on the list
        print("Refreshing page...")
        driver.refresh()
        wait_page_load(driver, table_view)
        # get table of available jobs
        print("Looking for jobs...")
        table_jobs = driver.find_elements_by_xpath(
            '//*[@class="x-grid-item-container"]')
        num_jobs = len(table_jobs)
        print(str.format("{0} jobs found", num_jobs))
        if(num_jobs > 0):
            break
    print("Fetching the first job...")
    # TODO
