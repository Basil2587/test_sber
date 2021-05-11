# Это приложение парсинга сайта: 
      http://reestr.nostroy.ru

#### Для работы кода нужны библиотеки: requests, BeautifulSoup, pandas.

На вход подается номер ИНН или список номеров через пробел, вытаскивается определенная информация и выгружается в базу данных с именем pars_data.db




### Подробно о работе кода.
    Загружаем номера ИНН и циклом for проходим по каждому номеру.
    С помощью функции get_html(url) делаем запрос нужной страницы и переводим ее в текст. 
    Подставляем наш текст в функции по поиску определенных тегов (
            def get_date(html), find_archive(page_archive), find_right(page_right)). 
    После того как сделали отбор по поиску тегов, подставляем в функции парсинга по отбору нужной информации с различных страниц (def parse_table(table), parse_page_2(page_2), parse_page_arch(page_arch), parse_page_right(page_right)). 
    Мы получили таблицы данных, объединяем их df = pd.concat([res, data_date, archive, the_right], axis=1). 
    Добавляем всё в DataFrame и выгружаем в базу данных с именем pars_data.db.