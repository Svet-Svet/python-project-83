import pytest_mock
import pytest
import string
import datetime

from unittest import mock

from page_analyzer.app import app
from page_analyzer.additional_func import normalize_url
from page_analyzer.check import fill_answer


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


def test_checking_add_seo():
    html_object = 'tests/fixtures/test_data.html'
    with open(html_object, encoding='utf8') as f:
        html = f.read()
    h1_tag, title_tag, str_meta = fill_answer(html)
    assert h1_tag == "Онлайн-школа программирования, за выпускниками которой охотятся компании"
    assert title_tag == "Хекслет — больше чем школа программирования. Онлайн курсы, сообщество программистов"
    assert str_meta == 'Живое онлайн сообщество программистов и разработчиков на JS, Python, Java, PHP, Ruby. Авторские программы обучения с практикой и готовыми проектами в резюме. Помощь в трудоустройстве после успешного окончания обучения'


def test_post_urls_long_url(client):
    test_url = string.ascii_letters * (256 // len(string.ascii_letters) + 1)
    response = client.post('/urls', data={"url": f'https://www.google.com/search?q{test_url}'}, follow_redirects=True)
    assert 'URL превышает 255 символов' in response.text


@mock.patch('psycopg2.connect')
def test_post_urls_exist_url(mock_connect, client):
    urls = [(1, 'https://www.google.com/', datetime.datetime(2022, 5, 18), )]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://www.google.com/search?'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 302


@mock.patch('psycopg2.connect')
def test_post_urls_new_url(mock_connect, client):
    urls = [(1000000, 'https://habr.com/ru/all/', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://habr.com/ru/all/'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 302


@mock.patch('psycopg2.connect')
def test_post_urls_new_url_error(mock_connect, client):
    urls = [(1000, 'https://12232312', datetime.datetime(2022, 5, 18),)]
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.__enter__.return_value.fetchall.return_value = urls

    test_url = 'https://12232312'
    response = client.post('/urls', data={"url": test_url})
    assert response.status_code == 422
