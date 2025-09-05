'''
This file Provides fixtures to set up a headless browser and page objects for each test.
Loads user data from CSV and initializes logging used across tests and page modules.
'''


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pages.login_page import Login
from pages.inventory_page import Inventory
from pages.cart_page import Cart
from pages.check_out import Checkout
from logging_helper import setup_logging
import pytest
import csv

@pytest.fixture(scope='function')
def browser():
    browser_settings = Options()   #creates a Chrome Options object, You're telling Selenium: “Hey, I want to customize how Chrome runs.”

    browser_settings.add_argument("--headless=new")  # ✅ Use the new, stable headless mode (required for Chrome 109+)
    browser_settings.add_argument("--window-size=1920,1080")  # ✅ Ensures full screen rendering to avoid click/interact issues
    browser_settings.add_argument("--disable-gpu")  # ✅ Fixes rendering issues in headless mode (mostly on Windows)
    browser_settings.add_argument("--no-sandbox")  # ✅ Required when running as root in Docker or Linux (avoids crashes)
    browser_settings.add_argument("--disable-dev-shm-usage")  # ✅ Prevents crashing due to limited /dev/shm in containers
    browser_settings.add_argument("--disable-extensions")  # 🧪 Speeds up loading by disabling all extensions
    browser_settings.add_argument("--disable-infobars")  # 🧪 Removes "Chrome is being controlled by automated test software"
    '''
    #optional if needed ... some elements create a issue 
    browser_settings.add_argument("--remote-allow-origins=*")  # 🧪 Fixes CORS issues in some newer Chrome versions (e.g., origin error)
    browser_settings.add_argument("--disable-software-rasterizer")  # 🧪 Helps with WebGL/canvas errors in graphics-heavy pages
    browser_settings.add_argument("--remote-debugging-port=9222")  # 🧪 Enables debugging, helpful if you want to inspect browser manually
    browser_settings.add_argument('--disable-blink-features=AutomationControlled')  # 🧪 Prevents basic bot detection (e.g., navigator.webdriver)
    '''

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_settings)
    #driver.maximize_window()
    yield driver
    driver.quit()


# This fixture initializes the browser and the page objects
@pytest.fixture(scope="function")
def setup_pages(browser):
    login_page = Login(browser)
    inventory_page = Inventory(browser)
    cart_page = Cart(browser)
    chqout = Checkout(browser)

    # Return them as a tuple so they can be used in the tests
    return login_page, inventory_page, cart_page, chqout

def load_test_data():
    with open("test_data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]    # List comprehension version  under id non compressed verson

        #data = []  # create empty list
        #for row in reader:  # loop through each row
            #data.append(row)  # add row to the list
        #return data  # return the full list

def pytest_generate_tests(metafunc):
    if "user_data" in metafunc.fixturenames:
        metafunc.parametrize("user_data", load_test_data())


setup_logging()# ✅ Initializes logging when pytest starts




