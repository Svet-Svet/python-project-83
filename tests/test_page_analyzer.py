import os
import pytest
import string
import datetime

from unittest import mock

from page_analyzer.app import app
from page_analyzer.additional_func import normalize_url
from page_analyzer.check import extract_metadata


@pytest.fixture()
def test():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    yield test_app


@pytest.fixture()
def client(test):
    return test.test_client()


def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_request_urls(client):
    response = client.get("/")
    assert response.status_code == 200


def test_normalize_url():
    test_url = 'https://ru.hexlet.io/blog/posts/programmirovanie-na-python-osobennosti-obucheniya-perspektivy-situatsiya-na-rynke-truda'
    response = normalize_url(test_url)
    assert response == 'https://ru.hexlet.io'


@pytest.fixture
def html_test_data():
    html_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data.html')
    with open(html_file, encoding='utf8') as f:
        html = f.read()
    return html


def test_checking_add_seo(html_test_data):
    h1_tag, title_tag, str_meta = extract_metadata(html_test_data)
    assert h1_tag == "Онлайн-школа программирования, за выпускниками которой охотятся компании"
    assert title_tag == "Хекслет — больше чем школа программирования. Онлайн курсы, сообщество программистов"
    assert str_meta == 'Живое онлайн сообщество программистов и разработчиков на JS, Python, Java, PHP, Ruby. Авторские программы обучения с практикой и готовыми проектами в резюме. Помощь в трудоустройстве после успешного окончания обучения'


def test_post_urls_long_url(client):
    test_url = string.ascii_letters * (256 // len(string.ascii_letters) + 1)
    response = client.post('/urls', data={"url": f'https://www.google.com/search?q{test_url}'}, follow_redirects=True)
    assert 'URL превышает 255 символов' in response.text


@mock.patch('psycopg2.connect')
def test_post_urls_exist_url(mock_connect, client):
    urls = [(1, 'https://www.google.com/', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://www.google.com/search?'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 302


@mock.patch('psycopg2.connect')
def test_post_urls_exist_url_flash_response(mock_connect, client):
    urls = [(1, 'https://www.google.com/', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.side_effect = [
        [(True,)],
        urls,
        urls,
        []
    ]
    test_url = 'https://www.google.com/search?'
    response = client.post('/urls', data={"url": test_url}, follow_redirects=True)
    assert 'Страница уже существует' in response.text


@mock.patch('psycopg2.connect')
def test_post_urls_new_url(mock_connect, client):
    urls = [(1000000, 'https://habr.com/ru/all/', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://habr.com/ru/'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 302


@mock.patch('psycopg2.connect')
def test_post_urls_new_url_flash_response(mock_connect, client):
    urls = [(1000000, 'https://habr.com/ru/', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.side_effect = [
        [(False,)],
        urls,
        []
    ]
    test_url = 'https://habr.com/ru/'
    response = client.post('/urls', data={"url": test_url}, follow_redirects=True)
    assert 'Страница успешно добавлена' in response.text


@mock.patch('psycopg2.connect')
def test_post_urls_new_url_error(mock_connect, client):
    urls = [(1000, 'https://12232312', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://12232312'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 422


@mock.patch('psycopg2.connect')
def test_post_urls_new_url_error_flash_response(mock_connect, client):
    urls = [(1000, 'https://12232312', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.side_effect = [
        [(False,)],
        urls,
        []
    ]
    test_url = 'https://12232312'
    response = client.post('/urls', data={"url": test_url}, follow_redirects=True)
    assert 'Некорректный URL' in response.text
