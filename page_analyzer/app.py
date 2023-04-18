import os

from flask import Flask, render_template, request
from flask import redirect, url_for, flash, g
from requests.exceptions import RequestException
from dotenv import load_dotenv
import validators
import requests

from page_analyzer.additional_func import normalize_url
from page_analyzer.check import fill_answer

from page_analyzer import db


load_dotenv()
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', '123456')
)

MAX_LENGHT_URL = 255
TIMEOUT = 5


def get_db():
    """ return object for communacation with BD"""
    database = getattr(g, '_database', None)
    if database is None or database.closed:
        database = g._database = db.get_connection()
    return database


@app.teardown_appcontext
def close_connection(exception):
    """Closed communacation with BD"""
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    url_name = request.form['url']

    if len(url_name) >= MAX_LENGHT_URL:
        flash('URL превышает 255 символов', 'error')
        return redirect(url_for('index'))

    if validators.url(url_name):
        connection = get_db()
        normalized_url = normalize_url(url_name)
        url_from_db = db.check_identity(connection, normalized_url)

        if url_from_db is not None:
            print(url_from_db)
            flash('Страница уже существует', 'success')
            id = url_from_db['id']
            return redirect(url_for('get_page', id=id))

        id = db.add_data(connection, normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_page', id=id))
    else:
        flash('Некорректный URL', 'error')
        return render_template('index.html'), 422


@app.get('/urls')
def get_urls():
    return render_template('urls.html', urls=db.get_all_pages(get_db()))


@app.get('/urls/<int:id>')
def get_page(id):
    connection = get_db()
    urls = db.get_page(connection, id)
    url_check = db.get_page_after_checking(connection, id)
    return render_template('urls_id.html', url=urls, url_for_check=url_check)


@app.post('/urls/<int:id>/checks')
def check_seo(id):
    connection = get_db()
    generally_page = db.get_page(connection, id)
    generally_id = generally_page[0]['id']
    generally_name = generally_page[0]['name']

    try:
        response = requests.get(generally_name, timeout=TIMEOUT)
        response.raise_for_status()
    except RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_page', id=generally_id))

    parser_status_code = response.status_code
    data_html = response.text
    h1_tag, title_tag, meta_tag = fill_answer(data_html)

    db.add_check_info(connection, generally_id, parser_status_code,
                      h1_tag, title_tag, meta_tag)

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_page', id=generally_id))


if __name__ == '__main__':
    app.run(debug=True)
