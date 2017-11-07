import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_info(clses, profs=None):
    driver = webdriver.PhantomJS()
    driver.get("https://pass.calpoly.edu")

    depts = [x.split()[0] for x in clses]
    print(depts)

    dept_selector = driver.find_element_by_xpath("//select[@data-filter='dept']") 

    num_courses = 0
    for option in dept_selector.find_elements_by_tag_name('option'):
        dept, ln = option.text.split("-")[:2]

        if dept in depts:
            print(option.text)
            option.click()
            course_list = driver.find_element_by_class_name("course-list")
            
            num_courses += click_courses(driver, [x.split()[1] for x in clses if dept in x], dept) 

    cart = driver.find_element_by_id("cart-list-view")
    assert num_courses == len(list(cart.find_elements_by_class_name("clearfix")))

    for cls in cart.find_elements_by_class_name("clearfix"):
        print(cls.find_element_by_class_name("left").text)

def click_courses(driver, courses, d):
    print(courses)

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

