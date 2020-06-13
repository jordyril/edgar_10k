import re
from bs4 import BeautifulSoup

import pandas as pd
import requests
from tqdm import tqdm

import os

DIRECTORY = "C:/Users/jrilla/OneDrive - bf.uzh.ch/SRP/Data/SEC_10k"
# DIRECTORY = "D:/OneDrive - bf.uzh.ch/SRP/Data/CDS"
os.chdir(DIRECTORY)


if not os.path.exists("Data/NasdaqNYSEAmex_ticker_name.pickle"):
    # Get all tickers for Nasdaq/NYSE/AMEX
    nasdaq_tickers = pd.read_csv(
        "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
    )
    nyse_tickers = pd.read_csv(
        "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
    )
    amex_tickers = pd.read_csv(
        "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"
    )
    # select proper columns
    nasdaq_tickers = nasdaq_tickers[["Symbol", "Name", "Sector", "industry"]]
    nyse_tickers = nyse_tickers[["Symbol", "Name", "Sector", "industry"]]
    amex_tickers = amex_tickers[["Symbol", "Name", "Sector", "industry"]]

    full_df = pd.concat([nasdaq_tickers, nyse_tickers, amex_tickers])
    full_df.drop_duplicates(inplace=True)
    full_df.rename({"Symbol": "Ticker"}, axis=1, inplace=True)
    full_df.sort_values("Ticker", inplace=True)
    full_df.reset_index(drop=True, inplace=True)
    full_df.to_pickle("Data/NasdaqNYSEAmex_ticker_name.pickle")

else:
    full_df = pd.read_pickle("Data/NasdaqNYSEAmex_ticker_name.pickle")

### GETTING CIK codes for each ticker
# ## OPTION 1
# ticker_cik_df1 = pd.read_csv("Data/cik_ticker.csv", sep="|")

# ticker_cik_df2 = pd.read_csv("Data/Ticker_Cik.csv")
# ticker_cik_df2["Ticker"] = ticker_cik_df2.ticker.str.upper()
# ticker_cik_df2.drop("ticker", axis=1, inplace=True)


# first_merge = full_df.merge(ticker_cik_df1, on="Ticker", suffixes=("", "2"))
# first_merge.drop("Name2", axis=1, inplace=True)
# sec_merge = full_df.merge(ticker_cik_df2, on="Ticker")

# full_df_merged = pd.concat([first_merge, sec_merge], sort=True)
# full_df_merged.drop_duplicates(subset=["Ticker", "CIK"], keep="first", inplace=True)
# full_df_merged.reset_index(inplace=True, drop=True)


# # change column order
# cols = full_df_merged.columns.tolist()
# print(cols)
# full_df_merged = full_df_merged[
#     [
#         "Ticker",
#         "CIK",
#         "Name",
#         "Business",
#         "SIC",
#         "IRS",
#         "Incorporated",
#         "Sector",
#         "industry",
#     ]
# ]

# full_df_merged.sort_values("Ticker", inplace=True)
# full_df_merged.reset_index(inplace=True, drop=True)

# # ALL THE ONE WITH MULTIPLE ENTRIES AND HENDE ONE WRONG CIK
# full_df_merged[full_df_merged.Ticker.duplicated(keep=False)].iloc[:, :3]
# full_df_merged[full_df_merged["Ticker"] == "AAC"]

# OPTION 2: via lookup on edgar
def MapTickerToCik(tickers):
    url = "http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany"
    cik_re = re.compile(r".*CIK=(\d{10}).*")

    ciks = []
    for ticker in tqdm(tickers):  # Use tqdm lib for progress bar
        results = cik_re.findall(requests.get(url.format(ticker)).text)
        if len(results):
            ciks.append(str(results[0]))
        else:
            ciks.append(None)

    ticker_cik_df = pd.DataFrame()
    ticker_cik_df["Ticker"] = tickers
    ticker_cik_df["CIK"] = ciks
    return ticker_cik_df


def map_ticker_to_edgar_info(tickers):
    URL = "http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany"

    cols = ["Name", "SIC", "CIK"]
    info_dic = {}
    for col in cols:
        info_dic[col] = []

    for ticker in tqdm(tickers):
        r = requests.get(URL.format(ticker))

        soup = BeautifulSoup(r.text, "lxml")

        info = soup.find("div", class_="companyInfo")

        if info is None:
            for i in cols:
                info_dic[i].append(None)

        else:
            try:
                span = info.find("span", class_="companyName")
                split = span.text.split("CIK#: ")

                info_dic["Name"].append(split[0].strip())
                info_dic["CIK"].append(split[1][:10])
            except:
                info_dic["Name"].append(None)
                info_dic["CIK"].append(None)

            try:
                p = info.find("p", class_="identInfo")
                a = p.find("a")
                info_dic["SIC"].append(a.text)
            except:
                info_dic["SIC"].append(None)

    summary_df = pd.DataFrame(index=tickers, columns=["Name", "SIC", "CIK"])
    for i in cols:
        summary_df[i] = info_dic[i]

    return summary_df.T


# if not os.path.exists("Output/_ticker_csv_option2.csv"):
#     ticker_cik_df3 = MapTickerToCik(list(full_df.Ticker))
#     ticker_cik_df3.dropna(inplace=True)
#     ticker_cik_df3.drop_duplicates(inplace=True)
#     ticker_cik_df3.reset_index(inplace=True, drop=True)
#     ticker_cik_df3.to_csv(f"Output/_ticker_csv_option2.csv", index=False)

# else:
#     ticker_cik_df3 = pd.read_csv("Output/_ticker_csv_option2.csv")


# ticker_cik_df3

# ticker_cik_name = ticker_cik_df3.merge(full_df, on="Ticker")
# ticker_cik_name.to_csv("Output/_ticker_cik_name.csv", index=False)

ticker_list = list(full_df["Ticker"])
# ticker_list = ["PLD"]
summary_df = map_ticker_to_edgar_info(ticker_list)

summary_df.to_pickle("Output/name_sic_cik_ticker_NasdaqNYSEAmex.pickle")

