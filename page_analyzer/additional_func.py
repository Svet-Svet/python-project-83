from urllib.parse import urlparse


def normalize_url(url):
    new_name = urlparse(url, "https")
    normal_url = f'{new_name.scheme}://{new_name.netloc}'
    return normal_url
