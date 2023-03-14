import requests

from bs4 import BeautifulSoup


def fill_answer(generally_name):
    obj_response = requests.get(generally_name, timeout=5)
    html = obj_response.text
    f = open('test.html', 'w')

    soup = BeautifulSoup(html, 'html.parser')

    h1_tag = soup.h1.get_text()
    title_tag = soup.title.get_text()
    meta_tag = soup.find('meta', attrs={'name': 'description'})

    str_meta = meta_tag['content'].strip()
    f.close()

    return h1_tag, title_tag, str_meta
