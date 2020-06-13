"""
BASED ON: https://community.mis.temple.edu/zuyinzheng/pythonworkshop/

This script looks for given ticker(s)/CIKs and form(s) and writes a csv-file with the links to
all the companies indexes. In a second script these index links will be used as inputs.

"""
import csv
import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# My own imports
from _support_functions import (
    create_logging,
    create_my_folders,
    intermediate_output_path,
)
from settings import forms, identifier
from settings import index_file_out as index_file
from settings import perform_index_link_scrape, ticker_cik_file

# =============================================================================
### PREAMBLE - prepare folders and set up log file
# =============================================================================
create_my_folders()
logger = create_logging(__name__, delete_previous=False)

# =============================================================================
### FUNCTIONS
# =============================================================================


def get_index_links(code, forms):
    """
    Looks for all index links (different years) for a given code (ticker or CIK) and form
    """
    EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb=&owner=exclude&count=100"
    # if forms is list like, will only search for first entry. e.g. when looking for 10-k, results
    # on edgar for other filings pop up and one could choose to also get these links
    url = EDGAR_URL.format(code, forms[0])
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("table", {"class": "tableFile2"})  # Table with information
    # Check if there is a table to extract / code exists in edgar database
    try:
        rows_in_table = table.findAll("tr")  # identify all rows in table
    except AttributeError:
        logger.warning(f"No tables found or no matching code symbol for {code}")
        return -1

    info_dic = {}
    i = 1
    for row in rows_in_table:  # itterate over all rows in tables
        cells = row.findAll("td")  # identify all cells in specific row
        if len(cells) == 5:  # If row has 5 , 2nd cell has wanted information

            # Check if file is actually the requested file
            form = cells[0].text.strip()
            logger.debug(f"{form}")
            if form in forms:

                # look for link where documents are stored
                link = cells[1].find("a", {"id": "documentsbutton"})
                logger.debug(f"link OK")

                # Construct link to documents
                doc_link = "https://www.sec.gov" + link["href"]
                logger.debug(f"doc_link OK")

                # Add description of files, strip take care of the space in the beginning and the end
                description = cells[2].text.encode("utf8").strip()
                logger.debug(f"description OK")

                # Date of filling, Change date format from 2012-1-1 to 2012_1_1
                filing_date = cells[3].text.strip()
                logger.debug(f"filling date OK")

                new_filing_date = filing_date.replace("-", "_")
                logger.debug(f"new filling date OK")

                info_dic[i] = [code, form, doc_link, description, new_filing_date]

                logger.debug(
                    f"{code}: {form} {doc_link}, {description}, {new_filing_date}"
                )

                i += 1

    return info_dic


# =============================================================================
### FILE CONFIGURATIONS
# =============================================================================
# standard format edgar url with blank spaces for the ticker/cik and form


# =============================================================================
### MAIN
# =============================================================================
logger.info(f"Process has started at {time.ctime()}")
start = datetime.datetime.now()


if perform_index_link_scrape:
    ticker_cik_df = pd.read_csv(intermediate_output_path(ticker_cik_file))
    codes = list(ticker_cik_df[identifier])

    with open(intermediate_output_path(index_file), mode="w", newline="") as output_csv:
        output_writer = csv.writer(
            output_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        output_writer.writerow(
            [f"{identifier}", "form", "index link", "description", "filing date"]
        )
        for code in tqdm(codes):
            links = get_index_links(code, forms)

            if not links == -1:
                for link in links:
                    output_writer.writerow(links[link])

else:
    pass

logger.info(f"Process has ended at {time.ctime()}")
end = datetime.datetime.now()

logger.info(f"Elapsed time: {end - start}")
logger.warning(f"END RUN \n")
