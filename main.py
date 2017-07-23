import requests
import yaml
from sys import exit
from bs4 import BeautifulSoup


def main() -> None:
    config = load_config()
    get_cheque()


def load_config() -> dict:
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f)
    except FileNotFoundError:
        exit('Please create a config file config.yml')

    return config


def get_cheque():
    page = requests.get('http://localhost:8000/')

    bs = BeautifulSoup(page.text.encode('iso8859-1', 'replace'), 'lxml')
    rows = bs.find('div', {'class': 'voucher_check'}).find_all('div', {'class': 'row'})

    for row in rows:
        name = row.find('div', {'class': 'col-xs-8'})
        if not name or name.text not in ['наименование товара', 'Количество', 'общая стоимость позиции с учетом скидок и наценок']:
            continue
        value = row.find('div', {'class': 'col-xs-4'})
        print(name.text + ': ' + value.text)


if __name__ == '__main__':
    main()
