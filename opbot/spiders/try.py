import datetime
import re
import time

import bs4
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

def parse(driver) -> dict:
    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    newitems = {}
    mainPage = soup.find(id="main")
    containerPage = mainPage.find("div", {"class":"shop-container"})
    products = containerPage.findAll("div", {"class":"product-small box"})
    print(f"This is the number of items : {len(products)}")
    for i, obj in enumerate(products):
        if i < 250:
            # newitems.update({i: obj})
            # newitems[i] = obj
            newitems.update({i: parse_result(obj)})

    # yield newitems
    print(newitems)

def parse_result(obj) -> dict:
    items = {}
    textContainer = obj.find("div", {"class":"box-text box-text-products"})
    nametag = obj.find("p", {"class":re.compile("^name.+")})
    # items["link1"] = it.find("a").attrs["href"]
    items["category"] = __safe_parsing(textContainer.find("p").text)
    items["img_url"] = __safe_parsing(obj.find("img").attrs["data-src"])
    items["name"] = __safe_parsing(nametag.text)
    items["link"] = __safe_parsing(nametag.find("a").attrs["href"])
    items["price"] = __safe_parsing(textContainer.find("bdi").text)
    items["dataID"] = __safe_parsing(textContainer.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-product_id"])
    items["sku"] = __safe_parsing(textContainer.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-product_sku"])
    items["quantity"] = __safe_parsing(textContainer.find("div", {"class":re.compile("^add-to-cart.+")}).find("a").attrs["data-quantity"])

    return items

def __safe_parsing(parsing) -> str:
    """
        assert if parsing arg is of type str, extract str from selector item if not
        Args:
          parsing(str): article from the crawler
        Returns:
          str: data from tag as a string
          none: no values retrieved from arg
        Raises:
          valueError: if instance is not str or Selector
    """
    try:
        if isinstance(parsing, str):
            return parsing
        elif isinstance(parsing, bs4.element.NavigableString):
            return parsing.strip()
        elif isinstance(parsing, scrapy.Selector):
            return parsing.get()
    except Exception:
        return None

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

        parse(driver)
    finally:
        # exit 
        driver.quit()


if __name__ == "__main__":
    connection()
