# edgar_10k
Scraping of 10K filings on EDGAR, code is mostly inspired by/based on [this code](https://community.mis.temple.edu/zuyinzheng/pythonworkshop/)
Code is from my earlier days, so some experimenting with unrelated things (like logging) + structure-wise I would do it differently these days.

## How to use:
1. Change `settings.py` to your liking (e.g. select steps you want to run or change filenames): 
    * Extra (self-explanatory) explanations in the file itself
    * Based on the info in `settings.py`, make sure you have the necessary files in `Output/`, e.g. if you have your own list of tickers/CIK's have it in csv format in `Output/` and specify the proper name in `settings.py`. (see `settings.py` for the naming conventions and assumed content in your csv-file)
    * I recommend not changing too much, basically you should make sure that the first step you want to run is properly set up, filenames for later steps are properly aligned at the moment so it's recommended to only change those if there is a strong preference for different filenames. 
 1. Run `MAIN.py` from the terminal
    * Creates all the intermediate files and when fully run, creates a folder with all the downloaded filings in html format
## Notes:
* If you are running the content of the folder on a cloud-based directory (like OneDrive or Dropbox), It's recommended to pause syncing while running `MAIN.py`


