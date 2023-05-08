from bs4 import BeautifulSoup


def extract_metadata(obj_html):
    soup = BeautifulSoup(obj_html, 'html.parser')

    h1_tag = soup.find('h1')
    if h1_tag is None:
        h1_tag = ''
    else:
        h1_tag = soup.h1.get_text()
        h1_tag = (h1_tag[:250] + '...') if len(h1_tag) > 250 else h1_tag
        h1_tag = h1_tag.strip()

    title_tag = soup.find('title')
    if title_tag is None:
        title_tag = ''
    else:
        title_tag = soup.title.get_text()
        title_tag = (title_tag[:250] + '...') if len(title_tag) > 250 else title_tag

    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag is None:
        str_meta = ''
    else:
        str_meta = meta_tag['content'].strip()
        str_meta = (str_meta[:250] + '...') if len(str_meta) > 250 else str_meta

    return h1_tag, title_tag, str_meta
