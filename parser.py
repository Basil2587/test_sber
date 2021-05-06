import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote


def parse_table(table):
    res = pd.DataFrame()
    id = 0
    name_org = ''
    inn = ''
    ogrn = ''
    status = ''
    type = ''
    reg_num = ''
    date_reg = ''
    date_close = ''

    data_tr = table.find('tr', {'class': 'sro-link'})
    name_org = data_tr.find_all('td')[1].text.replace('<br />', '\n').strip()
    inn = data_tr.find_all('td')[2].text.replace('<br />', '\n').strip()
    ogrn = data_tr.find_all('td')[3].text.replace('<br />', '\n').strip()
    status = data_tr.find_all('td')[4].text.replace('<br />', '\n').strip()
    type = data_tr.find_all('td')[5].text.replace('<br />', '\n').strip()
    reg_num = data_tr.find_all('td')[6].text.replace('<br />', '\n').strip()

    date_reg = list2[6]
    date_close_td = list2[7]
    if date_close_td is not None:
        date_close = date_close_td

    res = res.append(pd.DataFrame([[
        id, name_org, inn, ogrn, status, type,
        reg_num, date_reg, date_close]],
        columns=[
        'id', 'name_org', 'inn', 'ogrn', 'status',
        'type', 'reg_num', 'date_reg', 'date_close']), ignore_index=True)
    print(res)
    return(res)


if __name__ == '__main__':
    print("\n---------\n")
    num_inn = input("Введите ваш ИНН: ")
    # + '0278128540'
    print("\n---------\n")
    url_inn = '/reestr?m.fulldescription=&m.shortdescription=&m.inn='
    url = 'http://reestr.nostroy.ru'
    url_1 = url+(url_inn)+quote(num_inn)
    r = requests.get(url_1)
    with open('page1.html', 'w') as output_file:
        output_file.write(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    tables = soup.find_all('table', {'class': 'items'})
    rel_cl = [tag.get('rel')for tag in soup.find_all('tr')
                if not tag.get('rel')is None]
    num_clienta = rel_cl[0]
    url_2 = url + num_clienta
    t = requests.get(url_2)
    with open('page2.html', 'w') as output_file:
        output_file.write(t.text)
    soup2 = BeautifulSoup(t.text, 'lxml')
    tables2 = soup2.find_all('td')
    list2 = [p.text.strip() for p in soup2.find_all('td')if p.text is not None]

    result = pd.DataFrame()
    for item in tables:
        res = parse_table(item)
        result = result.append(res)

    result.to_excel('result.xlsx')
