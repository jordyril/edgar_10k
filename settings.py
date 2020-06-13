"""
NOTE 1: All input and intermediate output (used as input for next steps) files are saved as
'_filename' and will automatically be saved in this way as well.
However, they do not have to be written here with the underscore in front.
Remember that if not all steps are done using this code, your files
should be saved with the '_' in front of the name

NOTE 2: Not all steps have to be True, e.g. step A has already been done, it doesn't have to be
repeated, just give the filename of the original intermediate results and the other step can start
right away

NOTE 3: Notice that some files seem to be mentioned double here, different suffix (_out vs _in).
If fully run once, these files should just be the same,
however, for flexibility it is allowed to not
run the first step and use a previous results file for the next steps.
"""


### STEP A
forms = ["10-K"]  # list-like input
# can either be 'Ticker' or CIK', but in both cases your input file should contain an 'identifier' column
identifier = "CIK"

perform_index_link_scrape = True

# input file with tickers. should contain a column with header 'Ticker'
# ('CIK' column is redundant in this given file) and should be put in the
# 'OUTPUT' folder (since technically its and output of the 'get_cik_ticker_combinations' script
# but if not all tickers are wanted its better to create an own .csv file I guess)
# Again, do not forget to put it in the 'Output' folder and with '_' up front
# ticker_cik_file = "ticker_csv_option2.csv"
ticker_cik_file = "test.csv"

# intermediate output file used in step B
index_file_out = f"index_links_{identifier}.csv"  # default
# index_file_out = "index_links.csv"  # Results already saved

### STEP B
perform_form_link_scrape = True

# intermediate input file from step A
index_file_in = f"index_links_{identifier}.csv"  # default
# index_file_in = "index_links.csv"  # Results already saved

# intermediate output for step C
form_10k_file_out = f"index_links_form_10k_links_{identifier}.csv"  # default
# form_10k_file_out = "index_form_10k_links.csv"  # Results already saved

### STEP C
perform_form_html_download = False

# intermediate input file from step B
form_10k_file_in = f"index_links_form_10k_links_{identifier}.csv"  # default
# form_10k_file_in = "index_form_10k_links.csv"  # Results already saved

# final csv-file with all the summary information
html_file = f"full_summary_indexes_form_htmlpaths_{identifier}.csv"  # default
