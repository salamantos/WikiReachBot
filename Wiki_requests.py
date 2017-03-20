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

def open_url(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Достаем данные о текущей статье
        current_page_link = soup.find(rel="canonical").get('href')
        current_page_header = soup.find(id="firstHeading").get_text()
        print('Current Link is ' + current_page_link)
        print('Current Page is ' + str(current_page_header).decode('utf-8') + '\n')

        soup = soup.find(id="mw-content-text")
        a = soup.find_all('a')
    except Exception:  # AttributeError:
        return 'Wrong url', [], '', ''

    result = []
    link_id = 1
    for link in a:
        try:
            href = link.get('href')
            title = link.get('title')
            # inner_html = link.get_text()

            if not ('https' in href) and not (title is None):
                next_link = False
                for black_word in settings.black_list:
                    if black_word in title:
                        next_link = True
                    if 'img' in str(link):
                        next_link = True
                if not next_link:
                    result.append([link_id, title, href])
                    link_id += 1
        except TypeError:
            pass  # log_write('sys', 'EMPTY HREF!!!', sys_time())  # Не происходит из-за проверки not (title is None)
    return '', result, current_page_link, current_page_header
