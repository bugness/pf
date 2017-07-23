import os
import sys

import requests
import yaml
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl


def main() -> None:
    config = load_config()
    process_cheque_files(config['dir'], ext=config['file_ext'])


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

    for row in rows:
        name = row.find('div', {'class': 'col-xs-8'})
        if not name or name.text not in ['наименование товара', 'Количество', 'общая стоимость позиции с учетом скидок и наценок']:
            continue
        value = row.find('div', {'class': 'col-xs-4'})
        print(name.text + ': ' + value.text)


if __name__ == '__main__':
    main()
