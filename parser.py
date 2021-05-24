import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


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
        data_date = [p.text.strip()
                     for p in soup.find_all('td')if p.text is not None]
    except Exception.DoesNotExist:
        data_date = ''
    return data_date


def find_archive(page_archive):
    soup = BeautifulSoup(page_archive, 'lxml')
    try:
        data_arc = [p.text.replace('&downarrow;', '\n').strip()
                    for p in soup.find_all('td') if p.text is not None]
    except Exception.DoesNotExist:
        data_arc = ''
    return data_arc


def find_right(page_right):
    soup = BeautifulSoup(page_right, 'lxml')
    try:
        data_right = [p.text.replace('&downarrow;', '\n').strip()
                      for p in soup.find_all('table', {'class': 'items'})
                      if p.text is not None]
    except Exception.DoesNotExist:
        data_right = ''
    return data_right


def parse_table(table):
    # парсинг со страницы "реестр членов СРО" из 2 по 6 столбца информации
    res = pd.DataFrame()
    name_org = ''
    inn = ''
    ogrn = ''
    status = ''
    type = ''
    reg_num = ''

    data_tr = table.find('tr', {'class': 'sro-link'})
    name_org = data_tr.find_all('td')[1].text.strip()
    inn = data_tr.find_all('td')[2].text.strip()
    ogrn = data_tr.find_all('td')[3].text.strip()
    status = data_tr.find_all('td')[4].text.strip()
    type = data_tr.find_all('td')[5].text.strip()
    reg_num = data_tr.find_all('td')[6].text.strip()

    res = res.append(pd.DataFrame([[
        name_org, inn, ogrn, status, type,
        reg_num]],
        columns=[
        'name_org', 'inn', 'ogrn', 'status',
        'type', 'reg_num']))
    return res


def parse_page_2(page_2):
    # парсинг со страницы "Сведения о члене СРО" из 7 по 8 столбца информации
    res = pd.DataFrame()
    date_reg = ''
    date_close = ''

    date_reg = page_2[6]
    date_close_td = page_2[7]
    if date_close_td is not None:
        date_close = date_close_td

    res = res.append(pd.DataFrame(
        [[date_reg, date_close]],
        columns=['date_reg', 'date_close']), ignore_index=True)
    return res


def parse_page_arch(page_arch):
    # парсинг со страницы "Архив"
    res = pd.DataFrame()
    num_sv = ''
    date_open = ''
    basis = ''
    status_sv = ''

    num_sv = page_arch[7]
    date_open_td = page_arch[8]
    basis = page_arch[9]
    status_sv = page_arch[11]
    if date_open_td is not None:
        date_open = date_open_td

    res = res.append(pd.DataFrame([[
        num_sv, date_open, basis, status_sv]],
        columns=[
            'num_sv', 'date_open', 'basis', 'status_sv']), ignore_index=True)
    return res


def parse_page_right(page_right):
    # парсинг со страницы "Сведения о наличии права"
    res = pd.DataFrame()
    inform_of_the_right = ''
    inform_right = page_right[0]
    if inform_right is not None:
        inform_of_the_right = inform_right
    res = res.append(
        pd.DataFrame([[inform_of_the_right]], columns=['inform_of_the_right']))
    return res


def main():
    for i in num_inn:
        url_inn = base_url+(rel_inn)+i
        soup = BeautifulSoup(get_html(url_inn), 'lxml')
        tables = soup.find_all('table', {'class': 'items'})
        rel_cl = [tag.get('rel')for tag in soup.find_all('tr')
                  if not tag.get('rel') is None]
        num_clienta = rel_cl[0]
        url_client = base_url + num_clienta
        html = get_html(url_client)
        url_arch = url_client + '/certificates'
        url_of_the_right = url_client + '/rights'
        page_get_right = get_html(url_of_the_right)
        page_archive = get_html(url_arch)
        for item in tables:
            res = parse_table(item)
        data_date = parse_page_2(get_date(html))
        archive = parse_page_arch(find_archive(page_archive))
        the_right = parse_page_right(find_right(page_get_right))
        result = pd.DataFrame()
        df = pd.concat([res, data_date, archive, the_right], axis=1)
        result = result.append(df, ignore_index=True)
        engine = create_engine('sqlite:///pars_data.db')
        result.to_sql('users', con=engine, if_exists='append')


if __name__ == '__main__':
    base_url = 'http://reestr.nostroy.ru'
    rel_inn = '/reestr?m.fulldescription=&m.shortdescription=&m.inn='
    print("\n---------\n")
    num_inn = input("Введите ваш номер ИНН или список через пробел: ").split()
    # 0278128540 770965012811
    main()
    print("\n---------\n")
