import datetime
import re
import time

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instantiate options
# option = webdriver.ChromeOptions()
option = Options()
option.add_argument("--start-maximized") #open Browser in maximized mode
option.add_argument("--no-sandbox") #bypass OS security model
option.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)

def scroll(driver):
    scroll_pause_time = 1
    # get height of the screen 
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    # scroll infinitely to obtain items
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

def connection():
    try:
        # Load the HTML page
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    except Exception as err:
        print("Encountered an exception!!")
        raise err
    else:
        driver.get('https://copia.co.ke/product-category/all/saleable/foodstuff/cooking-oils/')
        time.sleep(10) # delay to allow webpage to load
        scroll(driver)

        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')

        mainPage = soup.find(id="main")
        containerPage = mainPage.find("div", {"class":"shop-container"})
        products = containerPage.findAll("div", {"class":"product-small box"})
        textContainer = containerPage.findAll("div", {"class":"box-text box-text-products"})
        nametag = containerPage.findAll("p", {"class":re.compile("^name.+")})
        # category = [art.find("p").text for art in textContainer]
        # link1 = [art.find("a").attrs["href"] for art in products]
        # img_url = [art.find("img").attrs["data-src"] for art in products]
        
        name = [art.text for art in nametag]
        link = [art.find("a").attrs["href"] for art in nametag]
        price = [art.find("bdi").text for art in textContainer]
        dataID = [art.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-product_id"] for art in textContainer]
        sku = [art.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-product_sku"] for art in textContainer]
        quantity = [art.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-quantity"] for art in textContainer]
        # print(f"This product: {name}-({link}) for {price}")
        # print(len(nametag))
        # print(nametag)
        
        
        # print(f"Found {len(link)} items \n{link} || {img_url}")
        # print(f"Found {len(img_url)} items \n{img_url}")
        print(f"Found {len(name)} items.")
    finally:
        # exit 
        driver.quit()


if __name__ == "__main__":
    connection()
