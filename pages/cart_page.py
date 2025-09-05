'''
Handles cart page actions like navigating to cart, checking cart status, counting items,
and removing the last item. Takes screenshots and logs key steps.
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from screenshot_helper import take_screenshot
import logging
import time
from screenshot_helper import take_screenshot

class Cart:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,30)

    def go_tocart(self):
        logging.info("going to click cart button")
        cart_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.shopping_cart_link")))
        self.driver.execute_script("arguments[0].click();", cart_button)
        take_screenshot(self.driver, "now on cart page")
        logging.info("cart button is clicked")

    def chq_cart(self):
        logging.info("on cart page")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="checkout"]')))
        #self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Your Cart']")))
        #return "cart" in self.driver.current_url
        #self.wait.until(EC.url_contains("cart"))
        logging.info("confirm cart url")
        return True




    def count_items(self):
        try:
            total = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
            return int(total.text)
        except TimeoutException:
            return 0

    def remove_item_by_name(self, item_name):
        # Force page render by scrolling

        logging.info("remove item function called")
        take_screenshot(self.driver, "before scroll")
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(0.5)
        #self.driver.execute_script("window.scrollTo(0, 0);")
        #take_screenshot(self.driver, "after scroll")
        #logging.info("screen is scrolled via java script")
        #cart_items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
        # ✅ Use CSS selector for precise targeting
        cart_items = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".cart_list .cart_item")))
            ##(By.CSS_SELECTOR, "div.cart_list > div.cart_item")   also can use this selector

        logging.info("found all elements on list")
        if not cart_items:
            logging.warning("cart is empty nothing to remove")
            return False

        #for item in cart_items:
            #name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            #if name == item_name:
        last_item = cart_items[-1]
        btn = last_item.find_element(By.TAG_NAME, "button")
        # ✅ Use JavaScript click to ensure success
        self.driver.execute_script("arguments[0].click();", btn)

        #self.wait.until(EC.element_to_be_clickable(btn))
                #if btn.text == "Remove":
                    #btn.click()
        logging.info("Last item in cart removed successfully.")
        take_screenshot(self.driver, "after_remove_click")
        return True
        #return False

        ####___________________________________________------------------------------------- next code
