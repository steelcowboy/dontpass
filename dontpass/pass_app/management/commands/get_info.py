import sys
import time
import os
import re
import datetime
from enum import IntEnum
from bs4 import BeautifulSoup, SoupStrainer 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class gridCols(IntEnum):
    SECTION = 0
    TYPE = 1
    CLSNUM = 2
    INST = 3
    OPEN_S = 4
    RES_S = 5
    SEAT_T = 6
    WAITING = 7
    STATUS = 8
    DAYS = 9
    START = 10
    END = 11
    BUILDING = 12
    ROOM = 13

def get_class_or_empty_list(obj):
    val = obj.get("class")
    return val if val else []


def get_info():
    ## AS OF 5/18/18
    SUMMER = 2186
    FALL = 2188
    ##

    class_blocks = [] 
    time.sleep(1)

    capab = DesiredCapabilities.CHROME
    # capab['chromeOptions'] = {'args': ['--headless']}

    driver = webdriver.Remote(command_executor="http://localhost:9515", desired_capabilities=capab)

    driver.get("https://pass.calpoly.edu")

    driver.execute_script(f"window.location.href='/?selectedTerm={FALL}'")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dismissNew"))
    )
    element.click()

    q_title = driver.find_element_by_class_name("pageTitleQuarter").text
    q_title = q_title[0] + q_title[len(q_title)-2:]

    dept_selector = driver.find_element_by_xpath("//select[@data-filter='dept']") 

    num_courses = 0
    for option in dept_selector.find_elements_by_tag_name('option'):
        dept, ln = option.text.split("-")[:2]
        option.click()
        click_courses(driver, dept) 


    # Go to next page
    driver.find_element_by_id("nextBtn").click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "select-course"))
    )
    
    now = datetime.datetime.now()
    timestamp = f"{now.year}{now.month}{now.day}-{now.hour}{now.minute}"
    html = driver.page_source
    with open(f"pass-{timestamp}.html", "w") as passfile:
        passfile.write(html)

    driver.close()

    class_blocks = parse_pass(html)

    return {"quarter": q_title, "classes": class_blocks}

def click_courses(driver, d):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "selectCol"))
    )
    # This is to wait for the table to fully load (the wait driver doesn't
    # always work if it was clicked before
    time.sleep(1)

    course_list = driver.find_element_by_class_name("course-list")

    
    for btn in course_list.find_elements_by_class_name("btn"):
        WebDriverWait(driver, 10).until(EC.visibility_of(btn))
        btn.click()

    time.sleep(1)

def parse_pass(html):
    num_sections = 0

    strainer = SoupStrainer("div", class_="select-course")

    soup = BeautifulSoup(html, 'html.parser', parse_only=strainer)
    for class_block in soup.children:
        sections = []

        class_name = class_block.h3.text
        name = class_name.split("-")[0]
        name = name.rstrip().lstrip()
        clsname = re.sub(' +',' ', name)

        for row in class_block("tr"):
            if "key-cancel" in get_class_or_empty_list(row): 
                continue

            # First need to see if this is a notes row or a data row
            start_elem = row.find("td", class_="sectionNumber")
            if start_elem == None:
                continue

            cols = list(row("td"))
            i = cols.index(start_elem)

            # For some reason a section has a * in it, remove anything that's not a number
            section_num = int(re.sub("[^0-9]", "", cols[i].text))
            status = cols[i+gridCols.STATUS].text.lstrip().rstrip()
            
            sections.append({
                "section": section_num, 
                "type": cols[i+gridCols.TYPE].text,
                "class_number": int(cols[i+gridCols.CLSNUM].text),
                "instructor": cols[i+gridCols.INST].text,
                "open_seats": int(cols[i+gridCols.OPEN_S].text),
                "reserved_seats": int(cols[i+gridCols.RES_S].text),
                "taken": int(cols[i+gridCols.SEAT_T].text),
                "waiting": int(cols[i+gridCols.WAITING].text),
                "status": status,
                "days": cols[i+gridCols.DAYS].text,
                "start_time": cols[i+gridCols.START].text,
                "end_time": cols[i+gridCols.END].text,
                "building": cols[i+gridCols.BUILDING].text,
                "room": cols[i+gridCols.ROOM].span.text,
                })

        # Add a 0.01 to fix division by 0 error, if the denominator is 0 the numerator is certainly 0 as well
        sections = sorted(sections, key=lambda k: (k["taken"]+k["waiting"])/(k["open_seats"]+k["reserved_seats"]+k["waiting"]+k["taken"]+0.01))
        result = {"title": clsname, "sections": sections}

        num_sections += 1

    print(num_sections)
