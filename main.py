import requests
from bs4 import BeautifulSoup


# cheque
def main() -> None:
    page = requests.get('http://localhost:8000/')

    bs = BeautifulSoup(page.text.encode('iso8859-1', 'replace'), 'lxml')
    rows = bs.find('div', {'class': 'voucher_check'}).find_all('div', {'class': 'row'})

    for row in rows:
        name = row.find('div', {'class': 'col-xs-8'})
        if not name or not name.text.startswith('наименование товара'):
            continue
        value = row.find('div', {'class': 'col-xs-4'})
        print(name.text + ': ' + value.text)


if __name__ == '__main__':
    main()
