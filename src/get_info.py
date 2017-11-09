import sys
import time
import pprint
from enum import IntEnum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def get_info(clses, profs=None):
    driver = webdriver.PhantomJS()
    driver.get("https://pass.calpoly.edu")

    found_classes = []

    depts = [x.split()[0] for x in clses]

    dept_selector = driver.find_element_by_xpath("//select[@data-filter='dept']") 

    num_courses = 0
    for option in dept_selector.find_elements_by_tag_name('option'):
        dept, ln = option.text.split("-")[:2]

        if dept in depts:
            option.click()
            course_list = driver.find_element_by_class_name("course-list")
            
            result = click_courses(driver, [x.split()[1] for x in clses if dept in x], dept) 

            # Remove non-existent courses
            if result:
                found_classes.append(clses[depts.index(dept)])
                num_courses += 1 

    cart = driver.find_element_by_id("cart-list-view")
    assert num_courses == len(list(cart.find_elements_by_class_name("clearfix")))

    for cls in cart.find_elements_by_class_name("clearfix"):
        print(cls.find_element_by_class_name("left").text)

    print(found_classes)
    
    # Go to next page
    driver.find_element_by_id("nextBtn").click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "select-course"))
    )
    
    driver.save_screenshot("class_grid.png")

    classes = driver.find_elements_by_class_name("select-course")
    print(classes)
    pp = pprint.PrettyPrinter(indent=4)

    for i, table in enumerate(classes):
        pp.pprint(parse_row(found_classes[i], table))

def click_courses(driver, courses, d):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "selectCol"))
    )
    # This is to wait for the table to fully load (the wait driver doesn't
    # always work if it was clicked before
    time.sleep(1)
    driver.save_screenshot(f"{d}-buttons.png")

    course_list = driver.find_element_by_class_name("course-list")
    
    for row in course_list.find_elements_by_tag_name("tr"):
        try:
            cols = list(row.find_elements_by_tag_name("td"))
            if len(cols) > 5 and cols[2].text in courses:
                cols[0].find_element_by_class_name("btn").click()
                return 1 
        except:
            driver.save_screenshot("screenshot.png")
            driver.close()
            sys.exit(1)
    
    return 0

def parse_row(clsname, table):
    sections = []
    result = {clsname: sections}

    for row in table.find_elements_by_tag_name("tr"):
        # First need to see if this is a notes row or a data row
        try:
            start_elem = row.find_element_by_class_name("sectionNumber")
        except:
            continue

        cols = list(row.find_elements_by_tag_name("td"))
        i = cols.index(start_elem)

        sections.append({
            "section": cols[i].text,
            "class_number": cols[i+gridCols.CLSNUM].text,
            "instructor": cols[i+gridCols.INST].text,
            "open_seats": cols[i+gridCols.OPEN_S].text,
            "reserved_seats": cols[i+gridCols.RES_S].text,
            "waiting": cols[i+gridCols.WAITING].text,
            "status": cols[i+gridCols.STATUS].text,
            "days": cols[i+gridCols.DAYS].text,
            "timespan": cols[i+gridCols.START].text + " - " + cols[i+gridCols.END].text
            })

    return result

