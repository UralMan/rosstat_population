import requests
import re

import os
import pandas as pd

def get_page(url):
    page = requests.get(url)
    print("Status code", page.status_code)
    return page


def get_links(page):
    regex = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
    all_links = re.findall(regex, page.text)
    db_links = [x for x in all_links if 'dbscripts' in x[2]]
    db_links = [f"{x[0]}://{x[1]}{x[2]}" for x in db_links]
    
    return db_links


def save_table_to_excel(df, file_name, region):
    if os.path.exists(file_name):
        with pd.ExcelWriter(file_name, engine="openpyxl", mode='a') as writer:
            df.to_excel(writer, sheet_name=region)
    else:
        df.to_excel(file_name, sheet_name=region)

