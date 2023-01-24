import requests
from bs4 import BeautifulSoup as BS4
import json

import config
import modules


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}


def main():
    for url_reg in config.URLS_reg[2:3]:
        print(url_reg)
        print()

        last_page = modules.find_last_page(url_reg)

        for page in range(1, 2): # last_page + 1
            url_page = f'{url_reg}&page={page}'
            print(url_page)

            INFO_in_one_page = modules.find_info_in_page(url_page)

        print(INFO_in_one_page)







if __name__ == '__main__':
    main()

