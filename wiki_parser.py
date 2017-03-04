from bs4 import BeautifulSoup
import urllib.request

black_list = ['Редактировать раздел', 'Википедия', 'Ссылки на источники',
              '(Страница отсутствует)', '(страница отсутствует)',
              'Просмотр этого шаблона']
random_page_link = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6' \
                   '%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87' \
                   '%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0' \
                   '%D0%BD%D0%B8%D1%86%D0%B0 '

link_to_open = 'https://ru.wikipedia.org/wiki/%D0%9B%D0%B8_%D0%A7%D0%B6%D1' \
               '%8D%D0%BD%D1%8C_(' \
               '%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D0%B5%D0%BB%D1%8C)'  #
# random_page_link
response = urllib.request.urlopen(link_to_open)
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

# Достаем данные о текущей статье
current_page_link = soup.find(rel="canonical").get('href')
current_page_header = soup.find(id="firstHeading").get_text()
print('Current Link is ' + current_page_link)
print('Current Page is ' + str(current_page_header) + '\n')

soup = soup.find(id="mw-content-text")
a = soup.find_all('a')
for link in a:
    try:
        href = link.get('href')
        title = link.get('title')
        inner_html = link.get_text()

        if not ('https' in href) and not (title is None):
            next_link = False
            for black_word in black_list:
                if black_word in title:
                    next_link = True
                if 'img' in str(link):
                    next_link = True
            if not next_link:
                print(title, '---', href)
    except TypeError:
        print('EMPTY HREF!!!')
