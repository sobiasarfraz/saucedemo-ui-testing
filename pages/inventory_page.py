'''
Handles inventory page actions: sorting, adding items to cart,
resetting the app state via sidebar, handling pop-ups, and checking images.
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
import time
import logging


class Inventory:
    def __init__(self,driver):
        self.driver = driver
        self.default_wait = WebDriverWait(driver, 35)
        self.quick_wait = WebDriverWait(driver, 20)

    def login_check(self):
        return "inventory" in self.driver.current_url


    def clear_fields(self):
        # Uses JavaScript clicks to bypass headless mode issues with sidebar animations on saucedemo.com
        #execute_script(): A Selenium method that runs JavaScript code in the browser.
        #"arguments[0].click();": JavaScript code that tells the browser to simulate a click on the element passed to it.
        hamburger = self.default_wait.until(
            EC.presence_of_element_located((By.ID, 'react-burger-menu-btn'))
        )

        logging.info("Hamburger menu button found, clicking with JavaScript")
        self.driver.execute_script("arguments[0].click();", hamburger)
        logging.info("Sidebar clicked")

        self.default_wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bm-menu-wrap')))
        logging.info("Sidebar is present")

        reset_link = self.default_wait.until(
            EC.presence_of_element_located((By.ID, 'reset_sidebar_link')))
        logging.info("Reset link found, clicking with JavaScript")
        self.driver.execute_script("arguments[0].click();", reset_link)
        logging.info("Reset link clicked")
        #reset_link.click()

        close_button = self.default_wait.until(
            EC.element_to_be_clickable((By.ID, 'react-burger-cross-btn')))
        logging.info("Close button found, clicking with JavaScript")
        self.driver.execute_script("arguments[0].click();", close_button)
        #close_button.click()
        logging.info("Sidebar closed successfully")





    def handle_alert_if_present(self):


        try:
            self.default_wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alrt_txt = alert.text
            logging.warning(f"Handled alert: {alrt_txt}")
            time.sleep(0.5)
            alert.accept()
            logging.info("Alert accepted.")
            return alrt_txt
        except TimeoutException:
            logging.info("No alert present.")
            return None
        except Exception as e:
            logging.error(f"Error handling alert: {str(e)}")
            return None


    def sort_by_price(self):

        try:
            dropdown = Select(self.default_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))))
            dropdown.select_by_value("lohi")

        #except UnexpectedAlertPresentException:
            logging.warning("unexpected alert pop up")
            self.handle_alert_if_present()

        except UnexpectedAlertPresentException as e:
            logging.warning(f"unexpected alert pop up {str(e)}")
            self.handle_alert_if_present()
        except Exception as e:
            logging.error(f" can't sort out: {str(e)}")

    def add_first_items(self):
        added_items = []
        cart_badge_selector = (By.CLASS_NAME, "shopping_cart_badge")
        last_cart_count = 0

        items = self.quick_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))

        for item in items:
            if len(added_items) >= 3:
                break
            try:
                name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                button = item.find_element(By.TAG_NAME, "button")
                self.quick_wait.until(EC.element_to_be_clickable(button))
                #button.click()
                self.driver.execute_script("arguments[0].click();", button)  # ✅ JavaScript click

                # Wait shortly for cart badge to update
                for _ in range(6):
                    try:
                        badge = self.driver.find_element(*cart_badge_selector)
                        count = int(badge.text)
                        if count > last_cart_count:
                            last_cart_count = count
                            added_items.append(name)
                            break
                    except:
                        pass
                    time.sleep(0.5)

            except Exception as e:
                logging.warning(f"Could not add item {name}: {str(e)}")
                continue

        return added_items
                
                


    def image_check(self):
        try:
            #images = self.default_wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='inventory_item_img']//img")))  # can use alone this path as parent child Xpath no need under loop
            images = self.default_wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='inventory_item_img']")))
        except TimeoutException:
            return ["Timeout waiting for image elements to load."]
        broken_images = []
        for index, image in enumerate(images):
            try:
                img_link = self.quick_wait.until(EC.presence_of_element_located((By.XPATH, ".//img")))
                #img_link = self.default_wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='inventory_item_img']//img")))
                src_link = img_link.get_attribute("src")
                if not src_link or not img_link.is_displayed():
                    broken_images.append(f"image at index no: {index}  is missing or broken,  src: {src_link}")
            except Exception as e:
                broken_images.append(f"Failed to check image at index {index + 1}: {str(e)}")
        return broken_images






