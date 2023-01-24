import requests
from bs4 import BeautifulSoup as BS4
import json
import os
import time


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}


def get_html(url):
    r = requests.get(url, headers=HEADERS, proxies={'https': f'http://{get_prox()}'})
    soup = BS4(r.text, 'lxml')
    return soup


def get_prox():
    # Получаем полный путь к дирректории
    dir_path = os.path.dirname(os.path.abspath(__file__))

    try:
        with open(os.path.join(dir_path, 'Proxy.json'), 'r', encoding='utf-8') as file:
            proxi = json.load(file)
    except:
        try:
            time.sleep(0.5)
            with open(os.path.join(dir_path, 'Proxy.json'), 'r', encoding='utf-8') as file:
                proxi = json.load(file)
        except:
            try:
                time.sleep(0.5)
                with open(os.path.join(dir_path, 'Proxy.json'), 'r', encoding='utf-8') as file:
                    proxi = json.load(file)
            except:
                time.sleep(0.5)
                with open(os.path.join(dir_path, 'Proxy.json'), 'r', encoding='utf-8') as file:
                    proxi = json.load(file)

    last = proxi['last']
    if int(last) < 5:
        proxi['last'] = str(int(last) + 1)
    else:
        proxi['last'] = '1'

    with open(os.path.join(dir_path, 'Proxy.json'), 'w', encoding='utf-8') as file:
        json.dump(proxi, file, indent=3, ensure_ascii=False)

    # print(proxi[last])
    return proxi[last]


def find_last_page(url):
    soup = get_html(url)

    last_page = soup.find('div', class_='pager').find_all('li')[-1].text.strip()
    return int(last_page)


def find_info_in_page(url):
    soup = get_html(url)

    conts = soup.find('div', class_='a-list').find_all('div', class_='a-card')
    print(len(conts))

    ALL_info_in_one_page = []

    for cont in conts:
        info = {}

        script_html = cont.find('script', type='text/javascript')
        script_json = json.loads(script_html.text.strip().split('.push(')[1].split(');')[0])

        try:
            avgPrice = int(script_json['attributes']['avgPrice'])
        except KeyError:
            continue

        unitPrice = int(script_json['unitPrice'])
        absU = round(float(100 - ((unitPrice * 100) / avgPrice)), 2)

        if absU >= 8:

            info = {
                'name': script_json['name'],
                'href': f"https://kolesa.kz/a/show/{script_json['id']}",
                'price': script_json['unitPrice'],
                'avgPrice': avgPrice,
                'absU': absU,
                'region': script_json['region'],
                'city': script_json['city'],
                'script': script_json
            }

            ALL_info_in_one_page.append(info)

    return ALL_info_in_one_page

def create_mes(INFO):
    MES = f'{INFO["name"]}\n' \
          f'{INFO["href"]}\n' \
          f'Цена: {INFO["price"]}\n' \
          f'Ср. Цена {INFO["avgPrice"]}\n' \
          f'Разница: {INFO["absU"]} %\n' \
          f'Регион: {INFO["region"]}\n' \
          f'Город: {INFO["city"]}\n'

    return MES


















