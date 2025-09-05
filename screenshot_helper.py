'''
Creates screenshots folder if needed.
Saves a screenshot with a timestamped filename from the given driver.
'''

import os
from datetime import datetime

os.makedirs("screenshots", exist_ok=True)
def take_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename
