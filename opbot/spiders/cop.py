import os
import time

# import pyautogui
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Instantiate options
# option = webdriver.ChromeOptions()
option = Options()
option.add_argument("--start-maximized") #open Browser in maximized mode
option.add_argument("--no-sandbox") #bypass OS security model
option.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)

def connection():
    try:
        # Load the HTML page
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
        # driver = webdriver.PhantomJS()
    except Exception as err:
        print("Encountered an exception!!")
        raise err
    else:
        driver.get('https://copia.co.ke/product-category/all/saleable/foodstuff/cooking-oils/')
        time.sleep(10)
        # timeout = 10
        # WebDriverWait(driver, timeout)
        # WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, 'container')))
        scroll_pause_time = 2
        # get height of the screen 
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1

        while True:
            # scroll one screen height at a time 
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')

        mainPage = soup.find(id="main")
        containerPage = mainPage.find("div", {"class":"shop-container"})
        # cont2 = containerPage.find("div", {"class":"products row row-small large-columns-4 medium-columns-4 small-columns-2 equalize-box"})
        # cont3 = cont2.find("div", {"class":"product-small col has-hover product type-product post-388067 status-publish first instock product_cat-cooking-oils has-post-thumbnail shipping-taxable purchasable product-type-simple"})
        # cont4 = containerPage.findAll("div", {"class":"product-small box"})

        # containers = soup.find()
        # print(soup.title)
        print(containerPage)
    finally:
        # exit 
        driver.quit()


if __name__ == "__main__":
    connection()
