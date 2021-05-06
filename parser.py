import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
        print(r.text)
    if r.status_code == 404:
        print('Страница не существует!')


def get_date(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        data_date = [p.text.strip() for p in soup.find_all('td')
            if p.text is not None]
    except Exception.DoesNotExist:
        data_date = ''
    return data_date


def parse_table(table):
    res = pd.DataFrame()
    id = 0
    name_org = ''
    inn = ''
    ogrn = ''
    status = ''
    type = ''
    reg_num = ''

    data_tr = table.find('tr', {'class': 'sro-link'})
    name_org = data_tr.find_all('td')[1].text.replace('<br />', '\n').strip()
    inn = data_tr.find_all('td')[2].text.replace('<br />', '\n').strip()
    ogrn = data_tr.find_all('td')[3].text.replace('<br />', '\n').strip()
    status = data_tr.find_all('td')[4].text.replace('<br />', '\n').strip()
    type = data_tr.find_all('td')[5].text.replace('<br />', '\n').strip()
    reg_num = data_tr.find_all('td')[6].text.replace('<br />', '\n').strip()

    res = res.append(pd.DataFrame([[
        id, name_org, inn, ogrn, status, type,
        reg_num]],
        columns=[
        'id', 'name_org', 'inn', 'ogrn', 'status',
        'type', 'reg_num']), ignore_index=True)
    print(res)
    return(res)


def parse_page_2(page_2):
    res = pd.DataFrame()
    date_reg = ''
    date_close = ''
    date_reg = page_2[6]
    date_close_td = page_2[7]
    if date_close_td is not None:
        date_close = date_close_td

    res2 = res.append(pd.DataFrame([[
         date_reg, date_close]],
        columns=[
         'date_reg', 'date_close']), ignore_index=True)
    print(res2)
    return(res2)


def main():
    print("\n---------\n")
    num_inn = input("Введите ваш ИНН: ")
    # + '0278128540'
    print("\n---------\n")
    return num_inn


if __name__ == '__main__':
    url = 'http://reestr.nostroy.ru'
    rel_inn = '/reestr?m.fulldescription=&m.shortdescription=&m.inn='
    url_inn = url+(rel_inn)+quote(main())
    soup = BeautifulSoup(get_html(url_inn), 'lxml')
    tables = soup.find_all('table', {'class': 'items'})
    rel_cl = [tag.get('rel')for tag in soup.find_all('tr')
                if not tag.get('rel')is None]
    num_clienta = rel_cl[0]
    url_client = url + num_clienta
    html = get_html(url_client)
    page_2 = get_date(html)
    result = pd.DataFrame()
    for item in tables:
        res = parse_table(item)
        result = result.append(res)
    data_date = parse_page_2(page_2)
    result = result.append(data_date)
    result.to_excel('result.xlsx')
