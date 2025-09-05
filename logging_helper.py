'''
Sets up logging to write INFO level logs to a timestamped file in the logs folder.
Creates the logs directory if it doesn't exist.
'''

import os
from datetime import datetime
import logging

def setup_logging():
    os.makedirs("logs", exist_ok=True)  # make log folder if not created
    filename = f"logs/log_{datetime.now().strftime('%y-%m-%d_%H-%M-%S')}.log"  # log path with timestamp, now() access current time & strftime() format that time
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",)