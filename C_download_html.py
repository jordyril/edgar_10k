"""
BASED ON: https://community.mis.temple.edu/zuyinzheng/pythonworkshop/

This script fetches the form (only in .html for now) from the links from step B and saves them locally
"""
import datetime
import logging
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from _support_functions import (
    create_logging,
    create_my_folders,
    create_subfolder,
    intermediate_output_path,
    output_path,
)
from settings import identifier
from settings import form_10k_file_in as form_10k_file
from settings import html_file, perform_form_html_download

# =============================================================================
### PREAMBLE - prepare folders and set up log file
# =============================================================================
# logging
create_my_folders()
logger = create_logging(__name__, level=logging.INFO)
# =============================================================================
### Functions
# =============================================================================
def download_form_html(data_dict):
    """
    given a dictionary with the following information: 'form', 'Code', 'year' and 'form link', 
    this function will save all form into an organised folder
    """
    # load information needed
    form = data_dict["form"]
    form_link = data_dict["form link"]
    year = data_dict["year"]
    code = data_dict[identifier]

    # create specific folder to save everything
    folder = f"{form.replace('-', '')}_HTML/{code}/"
    create_subfolder(folder)

    try:
        # check if download already exists
        html_name = f"{code}_{form.replace('-', '')}_{year}.htm"
        logger.debug(html_name)
        html_path = f"{folder}{html_name}"
        logger.debug(html_path)

        path_exists_already = os.path.exists(html_path)
        logger.debug(path_exists_already)
        if not path_exists_already:

            # read link/html page
            r = requests.get(form_link)
            logger.debug(r.status_code)

            # download locally
            html_file = open(html_path, "w")
            html_file.write(r.text)
            html_file.close()

        return html_path

    except:
        logger.error(f"{html_name} has not been downloaded")
        return None


# =============================================================================
### MAIN
# =============================================================================
logger.info(f"Process has started at {time.ctime()}")
start = datetime.datetime.now()

if perform_form_html_download:
    # read in results from step 2
    index_form_links = pd.read_csv(
        intermediate_output_path(form_10k_file), dtype=object
    )

    html_file_paths = []
    for row in tqdm(range(len(index_form_links))):
        # For now, can only properly download and save .htm/.html files

        if ".htm" in f'{index_form_links.iloc[row]["form name"]}':
            html_file_path = download_form_html(index_form_links.iloc[row].to_dict())

        elif ".txt" in f'{index_form_links.iloc[row]["form name"]}':
            html_file_path = None
            logger.warning(
                f"{index_form_links.iloc[row][identifier]} {index_form_links.iloc[row]['year']} not downloaded: \".txt\""
            )

        else:
            html_file_path = None
            logger.warning(
                f"{index_form_links.iloc[row][identifier]} {index_form_links.iloc[row]['year']} not downloaded: \"no format\""
            )

        html_file_paths.append(html_file_path)

        # save intermediate results in case of issues
        preliminary_results = index_form_links.iloc[: row + 1].copy()
        preliminary_results["html_file_path"] = html_file_paths
        preliminary_results.to_csv(
            intermediate_output_path(f"{html_file.split('.csv')[0]}_preliminary.csv"),
            index=False,
        )

    index_form_links["html_file_path"] = html_file_paths

    index_form_links.to_csv(output_path(html_file), index=False)
else:
    pass


logger.info(f"Process has ended at {time.ctime()}")
end = datetime.datetime.now()

logger.info(f"Elapsed time: {end - start}")
logger.warning(f"END RUN \n")
