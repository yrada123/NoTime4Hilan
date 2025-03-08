import json
from random import choices

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

######################
# Handling table
######################

# ignores already filled days and empty table cells
def filter_days(days):
    good_days = []
    for day in days:
        filled_hours = day.find_elements(By.CLASS_NAME, 'cDM')
        if filled_hours:
            filled_hours_txt = re.sub(r"\s+", "", filled_hours[0].text)
            if not filled_hours_txt:
                good_days.append(day)
    return good_days


def select_dates(driver, conf):
    if conf['is_last_month'] == 'True':
        prev_button = driver.find_elements(By.ID, 'ctl00_mp_calendar_prev')[0]
        prev_button.click()
        time.sleep(1)
    actions = ActionChains(driver)
    calendar = driver.find_elements(By.ID, "calendar_container")[0]

    # unmark today
    if conf['is_last_month'] != 'True':
        current_day = calendar.find_elements(By.CLASS_NAME, "currentDay")[0]
        while "CSD" in current_day.get_attribute("class"):
            actions.click(current_day).perform()

    # fetch table cells which are not holidays
    days = calendar.find_elements(By.CLASS_NAME, "cDIES")
    good_days = filter_days(days)

    # marking all days that are relevant
    all_days_marked = False
    while not all_days_marked:
        all_days_marked = True
        for day in good_days:
            if "CSD" not in day.get_attribute("class"):
                all_days_marked = False
                actions.click(day).perform()

    # clicking the add button
    buttons_container = driver.find_elements(By.ID, "ctl00_mp_upBtns")[0]
    buttons = buttons_container.find_elements(By.TAG_NAME, "input")
    for button in buttons:
        if button.get_attribute("value") == 'ימים נבחרים':
            button.click()
    time.sleep(2)

#########################
# handling filling hours
#########################

# edit hours
def fill_time_field(elm, text):
    elm.clear()
    for _ in range(5):
        elm.send_keys(Keys.LEFT)
    text = re.sub(r"\s+", "", text)
    elm.send_keys(text)

# filling selected days info
def fill_info(driver, conf):
    hours_div = driver.find_elements(By.ID, "MainDiv")[0]

    selects = hours_div.find_elements(By.TAG_NAME, "select")
    ### ignoring friday
    no_friday_selects = []
    for select in selects:
        parent = select
        while parent.tag_name != 'table':
            parent = parent.find_elements(By.XPATH, '..')[0]
        for _ in range(2):
            parent = parent.find_elements(By.XPATH, '..')[0]
        span = parent.find_elements(By.TAG_NAME, 'span')
        if not span:
            no_friday_selects.append(select)
        elif 'יום ו' not in span[0].text:
            no_friday_selects.append(select)

    ###  handles select buttons (presence type)
    trs = []
    for select_elm in no_friday_selects:
        try:
            select = Select(select_elm)
            select.select_by_value(conf['presence'])
            trs.append(select_elm.find_elements(By.XPATH, '../..')[0])
        except:
            pass

    ### setting hours and project code
    start_time = int(conf['start_time'].replace(':', ''))
    start_time = start_time // 100 + start_time % 100 / 60
    hours = float(conf['min_hours'])
    num_to_time = lambda x: str(int(x // 1 % 24)).zfill(2) + str(int(x % 1 * 60)).zfill(2)
    for tr in trs:
        inputs = tr.find_elements(By.TAG_NAME, 'input')

        today_start_time = start_time
        today_hours = hours
        # add random to hours if required
        if conf["is_random"] == 'True' and conf['start_time_distribution'] and conf['hours_distribution']:
            start_time_distribution = json.loads(conf['start_time_distribution'])
            hours_distribution = json.loads(conf['hours_distribution'])
            len_start = len(start_time_distribution)
            today_start_time = start_time + (choices(list(range(len_start)), start_time_distribution)[0] - (len_start-1) // 2) / 2
            len_hours = len(hours_distribution)
            today_hours = today_hours + choices(list(range(len_hours)), hours_distribution)[0] / 2

        # formatting and setting the time
        today_end_time = num_to_time(today_start_time + today_hours)
        today_start_time = num_to_time(today_start_time)
        fill_time_field(inputs[0], today_start_time)
        fill_time_field(inputs[1], today_end_time)

        # setting project
        inputs[5].send_keys(conf['project_code'])
        time.sleep(2)
        inputs[5].send_keys(Keys.ENTER)


    ### saving data
    for elm in hours_div.find_elements(By.TAG_NAME, 'input'):
        if elm.get_attribute('value') == 'שמירה':
            elm.click()
