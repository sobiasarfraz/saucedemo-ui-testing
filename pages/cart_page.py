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

        cart_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.shopping_cart_link")))
        self.driver.execute_script("arguments[0].click();", cart_button)
        take_screenshot(self.driver, "now on cart page")
        logging.info("cart button has been clicked")

    def chq_cart(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Your Cart']")))
        logging.info("confirm cart page title ")
        return True


    def count_items(self):
        try:
            total = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
            return int(total.text)
        except TimeoutException:
            return 0

    def remove_last_item(self):

        #  Use CSS selector for precise targeting
        cart_items = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".cart_list .cart_item")))
            ##(By.CSS_SELECTOR, "div.cart_list > div.cart_item")   also can use this selector

        logging.info("found all elements on list")
        if not cart_items:
            logging.warning("cart is empty nothing to remove")
            return False

        last_item = cart_items[-1]
        btn = last_item.find_element(By.TAG_NAME, "button")
        #  Use JavaScript click to ensure success
        self.driver.execute_script("arguments[0].click();", btn)

                    #btn.click()
        logging.info("Last item in cart removed successfully.")
        take_screenshot(self.driver, "after_removed_last_item")
        return True


