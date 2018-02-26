import sys
import time
import os
from enum import IntEnum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options

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

def get_info(clses):
    class_blocks = [] 
    found_classes = []
    
    opts = Options()
    opts.set_headless()
    driver = webdriver.Firefox(options=opts)

    driver.get("https://pass.calpoly.edu")

    depts = [x.split()[0] for x in clses]

    dept_selector = driver.find_element_by_xpath("//select[@data-filter='dept']") 

    driver.find_element_by_id("dismissNew").click()

    num_courses = 0
    for option in dept_selector.find_elements_by_tag_name('option'):
        dept, ln = option.text.split("-")[:2]

        if dept in depts:
            option.click()
            
            result = click_courses(driver, [x.split()[1] for x in clses if dept in x], dept) 

            # Remove non-existent courses
            if len(result):
                found_classes += result
                num_courses += 1 

    # cart = driver.find_element_by_id("cart-list-view")
    # assert num_courses == len(list(cart.find_elements_by_class_name("clearfix")))

    # Go to next page
    driver.find_element_by_id("nextBtn").click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "select-course"))
    )
    
    driver.save_screenshot("class_grid.png")

    classes = driver.find_elements_by_class_name("select-course")

    for i, table in enumerate(classes):
        class_blocks.append(parse_table(found_classes[i], table))
    
    driver.close()

    return class_blocks

def click_courses(driver, courses, d):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "selectCol"))
    )
    # This is to wait for the table to fully load (the wait driver doesn't
    # always work if it was clicked before
    time.sleep(1)
    # driver.save_screenshot(f"{d}-buttons.png")

    found_courses = [] 
    course_list = driver.find_element_by_class_name("course-list")
    
    for row in course_list.find_elements_by_tag_name("tr"):
        try:
            cols = list(row.find_elements_by_tag_name("td"))
            if len(cols) > 5 and cols[2].text in courses:
                cols[0].find_element_by_class_name("btn").click()
                found_courses.append(f"{d} {cols[2].text}")
        except:
            driver.save_screenshot("screenshot.png")
            driver.close()
            sys.exit(1)
    
    return found_courses 

def parse_table(clsname, table):
    sections = []

    for row in table.find_elements_by_tag_name("tr"):
        # First need to see if this is a notes row or a data row
        try:
            start_elem = row.find_element_by_class_name("sectionNumber")
        except:
            continue

        cols = list(row.find_elements_by_tag_name("td"))
        i = cols.index(start_elem)

        sections.append({
            "section": int(cols[i].text),
            "type": cols[i+gridCols.TYPE].text,
            "class_number": int(cols[i+gridCols.CLSNUM].text),
            "instructor": cols[i+gridCols.INST].text,
            "open_seats": int(cols[i+gridCols.OPEN_S].text),
            "reserved_seats": int(cols[i+gridCols.RES_S].text),
            "taken": int(cols[i+gridCols.SEAT_T].text),
            "waiting": int(cols[i+gridCols.WAITING].text),
            "status": cols[i+gridCols.STATUS].text,
            "days": cols[i+gridCols.DAYS].text,
            "start_time": cols[i+gridCols.START].text,
            "end_time": cols[i+gridCols.END].text,
            "building": cols[i+gridCols.BUILDING].text,
            "room": cols[i+gridCols.ROOM].find_elements_by_tag_name("span")[0].text,
            })

    # Add a 0.01 to fix division by 0 error, if the denominator is 0 the numerator is certainly 0 as well
    sections = sorted(sections, key=lambda k: (k["taken"]+k["waiting"])/(k["open_seats"]+k["reserved_seats"]+k["waiting"]+k["taken"]+0.01))
    result = {"title": clsname, "sections": sections}
    return result

