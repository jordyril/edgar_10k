"""
BASED ON: https://community.mis.temple.edu/zuyinzheng/pythonworkshop/

This script looks at the index links from step A and retrieves the EDGAR links to the actual form

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
    intermediate_output_path,
)
from settings import form_10k_file_out as form_10k_file
from settings import index_file_in as index_file
from settings import perform_form_link_scrape

# =============================================================================
### PREAMBLE - prepare folders and set up log file
# =============================================================================
# logging
create_my_folders()
logger = create_logging(__name__, level=logging.INFO)
# =============================================================================
### FUNCTIONS
# =============================================================================
def get_10k_link(doc_link, form):
    """
    Given an index link and wanted form, function retrieves link to form
    """
    r = requests.get(doc_link)
    logger.debug(f"NEW doc link: {doc_link}")
    logger.debug(f"doc link split{doc_link.split('/')}")

    soup = BeautifulSoup(r.text, "lxml")

    form_link, form_name = None, None
    # Check if there is a table to extract / code exists in edgar database
    try:
        table = soup.find("table", {"summary": "Document Format Files"})
    except:
        logger.warning(f"No tables found for link {doc_link}")
        return form_link, form_name

    # loop over all rows
    logger.debug("New table:")
    for row in table.findAll("tr"):
        logger.debug("new row")

        # loop over all columns (cells)
        cells = row.findAll("td")

        # check if correct table format
        logger.debug(f"{len(cells)}")

        if len(cells) == 5:
            # check correct fillings/form
            logger.debug(f"{cells[3].text.strip()}")
            if cells[3].text.strip() == form:

                link = cells[2].find("a")  # cell with link
                split_href = link["href"].split("/")
                logger.debug(f"length: {split_href}")

                if len(split_href) == 7:  # This means its a valid link
                    form_link = "https://www.sec.gov" + link["href"]
                    form_name = link.text.strip()
                    break

    logger.debug(f"final form link:{form_link}")
    logger.debug(f"final form name:{form_name}")
    if form_link is None:
        try:  # The link in the original cell is not valid, hence have t go to full document link in last row
            last_row = table.findAll("tr")[-1]
            last_cells = last_row.findAll("td")

            link = last_cells[2].find("a")  # cell with link

            form_link = "https://www.sec.gov" + link["href"]
            form_name = link.text.strip()

        except:
            logger.warning(f"No link found for {doc_link}")

    return form_link, form_name


# =============================================================================
### MAIN
# =============================================================================
logger.info(f"Process has started at {time.ctime()}")
start = datetime.datetime.now()

### Get Index links from step 1
index_links = pd.read_csv(intermediate_output_path(index_file))

# Instead of filing year, we want to know subject year of file
index_links["year"] = index_links["filing date"].apply(
    lambda x: int(x.split("_")[0].strip()) - 1
)
row = 299
index_form_links = index_links
### PERFORM STEP 2
if perform_form_link_scrape:
    form_links, form_names = [], []

    """
    If something would go wrong, change '..._intermediate' into '..._preliminary' and restart process, it will not redo
    its previous progress
    """
    if os.path.exists(
        intermediate_output_path(f"{form_10k_file.split('.csv')[0]}_preliminary.csv")
    ):
        previous_progress = pd.read_csv(
            intermediate_output_path(
                f"{form_10k_file.split('.csv')[0]}_preliminary.csv"
            )
        )
    else:
        previous_progress = None

    for row in tqdm(range(len(index_links))):
        index_link = index_links.iloc[row]["index link"]
        form = index_links.iloc[row]["form"]
        if previous_progress is not None:
            if index_link in list(previous_progress["index link"]):
                if (
                    previous_progress[previous_progress["index link"] == index_link][
                        "form"
                    ].values[0]
                    == form
                ):
                    form_link = previous_progress[
                        previous_progress["index link"] == index_link
                    ]["form link"].values[0]
                    form_name = previous_progress[
                        previous_progress["index link"] == index_link
                    ]["form name"].values[0]
                else:
                    form_link, form_name = get_10k_link(index_link, form)
        else:
            form_link, form_name = get_10k_link(index_link, form)

        form_links.append(form_link)
        form_names.append(form_name)

        # If something would go wrong, progress will be saved
        preliminary_results = index_form_links.iloc[: row + 1].copy()
        preliminary_results["form link"] = form_links
        preliminary_results["form name"] = form_names
        preliminary_results.to_csv(
            intermediate_output_path(
                f"{form_10k_file.split('.csv')[0]}_intermediate.csv"
            ),
            index=False,
        )

    index_form_links["form link"] = form_links
    index_form_links["form name"] = form_names

    index_form_links.to_csv(intermediate_output_path(form_10k_file), index=False)

else:
    pass

logger.info(f"Process has ended at {time.ctime()}")
end = datetime.datetime.now()

logger.info(f"Elapsed time: {end - start}")
logger.warning(f"END RUN \n")
