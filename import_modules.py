import csv
import json
import os
import pprint
import re
import threading
import time
import traceback
import urllib
from datetime import datetime
from functools import reduce
from time import sleep
from urllib.parse import unquote

import brotli
import pandas as pd
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from openpyxl import load_workbook

from constants import *
from jild_hadith_parsing import *

def protect_get_connection_error(url, header={}, tries=4, unlimited=False):
    stop_times = 0
    response = None
    while True and stop_times < tries:
        try:
            response = requests.get(url, headers=header)

            break
        except:
            if unlimited == False:
                stop_times += 1
            if response == None:
                traceback.print_exc()
                sleep(5*stop_times)
                continue

            if response.status_code != 200:
                traceback.print_exc()
                sleep(5*stop_times)
                continue
            else:
                break
    return response


def protect_post_connection_error(url, header, data, json_boolean, tries=4, unlimited=False):
    response = None
    stop_times = 0
    while True and stop_times < tries:
        try:
            if json_boolean == True:
                response = requests.post(url, json=data, headers=header)

            else:
                response = requests.post(url, data=data, headers=header)

            break
        except:
            if unlimited == False:
                stop_times += 1
            if response == None:
                traceback.print_exc()
                sleep(5*stop_times)
                continue
            if response.status_code != 200:
                traceback.print_exc()
                sleep(5*stop_times)
                continue
            else:
                break
    return response
