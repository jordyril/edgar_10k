"""
Created on Wed Jun 26 19:12:46 2019

@author: jrilla
"""
# =============================================================================
# PACKAGES
# =============================================================================
import os
import logging

# =============================================================================
# FUNCTIONS
# =============================================================================
def quote(string):
    return '"' + string + '"'


def create_subfolder(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


def create_outputfolder():
    create_subfolder("Output")


def create_logfolder():
    create_subfolder("Logs")


def create_my_folders():
    create_logfolder()
    create_outputfolder()


def create_logging(
    name,
    level=logging.INFO,
    formatting="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    delete_previous=False,
):

    # logging
    log_file = f"Logs/{name}.log"  # file name

    formatter = logging.Formatter(formatting)  # logging format

    logger = logging.getLogger(name)  # create logger
    logger.setLevel(level)

    writing_permission = "w" if delete_previous else "a"
    file_handler = logging.FileHandler(
        log_file, mode=writing_permission
    )  #'w' clears logs form previous runs
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def output_path(file_name):
    return f"Output/{file_name}"


def intermediate_output_path(file_name):
    return f"Output/_{file_name}"
