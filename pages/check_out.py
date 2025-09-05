'''
Manages checkout steps for different users: navigating checkout, validating and submitting forms,
completing orders, and logging out. Includes error handling, logging, and screenshots for tracking.
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging
from screenshot_helper import take_screenshot



class Checkout:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,30)
        self.short_wait = WebDriverWait(driver, 10)

    def chq_out(self):
        print("checkout function call")
        logging.info("checkout button function called")
        check_out_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="checkout"]')))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", check_out_btn)

        self.driver.execute_script("arguments[0].click();", check_out_btn)
        logging.info("check out button is clicked using java script")
        take_screenshot(self.driver, "on chcekout page ")
        time.sleep(1)

    def check_result(self):
        return "checkout" in self.driver.current_url

    def empty_form(self):
        take_screenshot(self.driver, "trial empty form")
        logging.info("first trying to fill empty form")
        continue_btn = self.wait.until(EC.element_to_be_clickable((By.NAME, "continue")))
        self.driver.execute_script("arguments[0].click();", continue_btn)
        take_screenshot(self.driver, "after clicking continue")
        error_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
        logging.info("click on continue and got error messgae of fill the form ... will return the error message")

        return error_field.text.strip()

    def fill_form(self,first,last,zip):
        logging.info("now again on empty form.. now will fill the form to give the data")
        take_screenshot(self.driver, "fill the form")
        first_name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#first-name")))
        last_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='lastName']" )))
        postal_code = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='postalCode']")))

        # JS script to set value and dispatch events

        js_code = """
          function setNativeValue(element, value) {
              const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value').set;
              const prototype = Object.getPrototypeOf(element);
              const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;

              if (valueSetter && valueSetter !== prototypeValueSetter) {
                  prototypeValueSetter.call(element, value);
              } else {
                  valueSetter.call(element, value);
              }
              element.dispatchEvent(new Event('input', { bubbles: true }));
              element.dispatchEvent(new Event('change', { bubbles: true }));
          }
          setNativeValue(arguments[0], arguments[1]);
          """
          #-------this was original now i am trying other to see if they work well----------


        '''
        js_code = """
           function setNativeValue(el, value) {
               const lastValue = el.value;
               el.value = value;
               let event = new Event('input', { bubbles: true });
               el.dispatchEvent(event);
               event = new Event('change', { bubbles: true });
               el.dispatchEvent(event);
           }
           setNativeValue(arguments[0], arguments[1]);
           """
           '''
       

        # Use proper JS setter for each input
        self.driver.execute_script(js_code, first_name, first)
        self.driver.execute_script(js_code, last_name, last)
        self.driver.execute_script(js_code, postal_code, zip)
        take_screenshot(self.driver, "enter data to form")
        logging.info("gave data to form")

        # Submit the form
        #self.driver.execute_script("document.querySelector('form').submit();")

        continue_btn_clck = self.wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn_clck)
        self.driver.execute_script("arguments[0].click();", continue_btn_clck)



        take_screenshot(self.driver, "after click continue btn filling the form")
        logging.info("fil the form and continue to click")
        try:
            error_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
            if "Error: Last Name is required" in error_btn.text:
                logging.warning(f"try to fill the form but got error: {error_btn.text}, not able to complete the order.moving to logout")
                return False
        except TimeoutException:
            return True
        except Exception as e:
            logging.error(f"Failed to fill form: {str(e)}")
            return False


    def overview(self):
        logging.info("overview function has called")
        #time.sleep(1)
        take_screenshot(self.driver, "on overview page")
        self.wait.until(EC.url_contains("checkout-step-two"))
        #return "checkout-step-two" in self.driver.current_url
        return True


    def finish_chqout(self):
        try:
            take_screenshot(self.driver,"finish page")
            finish_button = self.short_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Finish']")))
            self.driver.execute_script("arguments[0].click();", finish_button)
            take_screenshot(self.driver,"click on finish btn")
            #time.sleep(3)  # Wait for potential page change

            if "checkout-step-two" in self.driver.current_url:
                logging.warning("Finish button click had no effect, cannot proceed")
                return False
            order_done = self.short_wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[text()='Thank you for your order!']")))
            logging.info("Checkout successful")
            take_screenshot(self.driver, "order has been placed")
            return True
        except Exception as e:
            logging.error(f"Failed to finish checkout: {str(e)}")
            return False


    def log_out(self):
        logging.info("logout function called")
        menu_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='react-burger-menu-btn']")))
        logging.info("menue button detect")
        self.driver.execute_script("arguments[0].click();", menu_btn)
        logging.info("menue button clicked")

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bm-menu-wrap')))
        logging.info("Sidebar is present")

        logout_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='logout_sidebar_link']")))
        logging.info("logout button detectc")

        self.driver.execute_script("arguments[0].click();", logout_btn)
        logging.info("logout done")

    def confrm_logout(self):
        logging.info("confirm logout on main page funtion called")
        confrm = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Swag Labs']")))
        return confrm.text



