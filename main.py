import os
import sys
import sqlite3

import requests
import yaml
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl


def main() -> None:
    config = load_config()
    process_cheque_files(config['dir'], ext=config['file_ext'])
    # read_db()


def load_config() -> dict:
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f)
    except FileNotFoundError:
        sys.exit('Please create a config file config.yml')

    return config


def process_cheque_files(dir, ext='.txt') -> None:
    for file in os.listdir(dir):
        if file.endswith(ext):
            print(file)
            params = parse_cheque_file(os.path.join(dir, file))
            print(params)
            parse_cheque(params['fn'], params['fp'])


def parse_cheque_file(file) -> dict:
    with open(file, 'r') as txt:
        return dict(parse_qsl(txt.read()))


def parse_cheque(fn, fp) -> None:
    page = requests.get('https://lk.platformaofd.ru/web/noauth/cheque/', params={'fn': fn, 'fp': fp})

    bs = BeautifulSoup(page.text.encode('utf-8', 'replace'), 'lxml')
    rows = bs.find('div', {'class': 'voucher_check'}).find_all('div', {'class': 'row'})

    db = sqlite3.connect('data.db')
    cursor = db.cursor()

    item = list()

    for row in rows:
        name = row.find('div', {'class': 'col-xs-8'})
        if not name or name.text not in ['наименование товара', 'цена за единицу', 'Количество', 'общая стоимость позиции с учетом скидок и наценок']:
            continue
        item.append(row.find('div', {'class': 'col-xs-4'}).text)
        if len(item) == 4:
            cursor.execute('''INSERT INTO items (name, unit_price, qty, amount) VALUES (?, ?, ?, ?)''', item)
            item.clear()

    db.commit()
    db.close()


def setup_db() -> None:
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, unit_price TEXT, qty TEXT, amount TEXT)''')
    db.close()


def read_db() -> None:
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM items''')
    for item in cursor:
        print(item)
    db.close()


if __name__ == '__main__':
    main()
