# coding=utf-8
import sys
from bs4 import BeautifulSoup
import urllib2
import settings

reload(sys)
sys.setdefaultencoding('utf8')


# Модуль запросов к Википедии
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Открытие ссылки и извлечение информации со страницы
def open_url(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Достаем данные о текущей статье
        current_page_link = soup.find(rel="canonical").get('href')
        current_page_header = soup.find(id="firstHeading").get_text()
        print('Current Link is {}'.format(current_page_link))
        print('Current Page is {}\n'.format(current_page_header.decode('utf-8')))

        soup = soup.find(id="mw-content-text")
        a = soup.find_all('a')
    except Exception:  # AttributeError:
        return 'Wrong url', [], '', ''

    result = []
    link_id = 1
    # Формируем список ссылок, извлекаем адрес и название статьи
    for link in a:
        try:
            href = link.get('href')
            title = link.get('title')
            # inner_html = link.get_text()

            if not ('https' in href) and not (title is None):
                next_link = False
                for black_word in settings.BLACK_LIST:
                    if black_word in title:
                        next_link = True
                    if 'img' in str(link):
                        next_link = True
                if not next_link:
                    result.append([link_id, title, href])
                    link_id += 1
        except TypeError:
            pass
    return '', result, current_page_link, current_page_header
