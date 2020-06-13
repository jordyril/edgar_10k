import datetime
import logging
import os
import time

# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from tqdm import tqdm


from _support_functions import create_logging, create_my_folders

# =============================================================================
### PREAMBLE
# =============================================================================
create_my_folders()
logger = create_logging(__name__, level=logging.INFO)


# directory set
# DIRECTORY = r"C:\Users\jrilla\Desktop\10K"  # desktop
# DIRECTORY = "C:/Users/jordy/Dropbox/Jordy/10K"  # laptop
# os.chdir(DIRECTORY)


DIRECTORY = os.path.abspath(os.path.dirname(__file__))
logger.info(f"{DIRECTORY}")

# =============================================================================
### CORE
# =============================================================================
## General start
logger.info(f"Process has started at {time.ctime()}")
start = datetime.datetime.now()

# start script A
print("Progress Step A: Getting index links")
logger.info(f"Step A has started: {time.ctime()}")

import A_get_edgar_indexes

# end script A
logger.info("Step A has finished: {time.ctime()}")
print()

# start script B
print("Progress Step B:Getting form links")
logger.info("Step B has started: {time.ctime()}")

import B_get_10k_links

# end script B
logger.info(f"Step B has finished: {time.ctime()}")
print()

# start script C
print(f"Progress Step C: Downloading files")
logger.info(f"Step C has started: {time.ctime()}")

import C_download_html

# end script C
logger.info(f"Step C has finished: {time.ctime()}")
print()

## General end
logger.info(f"Process has ended at {time.ctime()}")
end = datetime.datetime.now()

logger.info(f"Elapsed time: {end - start}")
logger.warning(f"END RUN \n")
