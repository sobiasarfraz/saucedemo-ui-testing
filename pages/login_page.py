'''
Handles opening the login page, performing login actions,
and checking for login errors and messages.
'''

from selenium.webdriver.common.by import By
import time


class Login:
    def __init__(self,driver):
        self.driver = driver

    def open_browser(self):
        self.driver.get("https://www.saucedemo.com")

    def login(self,username,password):
        user = self.driver.find_element(By.XPATH, "//input[@id='user-name']")
        user.send_keys(username)
        paswod = self.driver.find_element(By.CSS_SELECTOR, "input#password")
        paswod.send_keys(password)
        time.sleep(0.5)
        buton = self.driver.find_element(By.CSS_SELECTOR, "input[type=submit]")
        buton.click()

    def is_error_found(self):
        try:
            error = self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            return True
        except:
            return False

    def error_message(self):
        try:
            message = self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            return message.text
        except:
            return ""
