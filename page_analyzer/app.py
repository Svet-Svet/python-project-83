from flask import Flask, render_template, request
from flask import redirect, url_for, flash

from page_analyzer.db import add_data, add_side, show_page
from page_analyzer.db import check_identity, check_site, show_page_checks

from page_analyzer.additional_func import normalize_url
from page_analyzer.check import fill_answer

from validators import url
from requests.exceptions import RequestException
import requests


app = Flask(__name__)
app.config.update(
    SECRET_KEY='123456'
)

MAX_LENGHT_URL = 255


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    url_name = request.form['url']

    if len(url_name) >= MAX_LENGHT_URL:
        flash('URL превышает 255 символов', 'error')
        return redirect(url_for('index'))

    if url(url_name):
        normal_name = normalize_url(url_name)
        url_from_db = check_identity(normal_name)

        if url_from_db is not False:
            flash('Страница уже существует', 'success')
            id = url_from_db[0]['id']
            return redirect(url_for('get_page', id=id))

        id = add_data(normal_name)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_page', id=id))
    else:
        flash('Некорректный URL', 'error')
        return redirect(url_for('index'))


@app.get('/urls')
def get_urls():
    return render_template('urls.html', urls=add_side())


@app.route('/urls/<int:id>', methods=['POST', 'GET'])
def get_page(id):
    urls = show_page(id)
    url_check = show_page_checks(id)
    return render_template('urls_id.html', url=urls, url_for_check=url_check)


@app.route('/urls/<int:id>/checks', methods=['POST', 'GET'])
def checks_site_data(id):
    generally_page = show_page(id)
    generally_id = generally_page[0]['id']
    generally_name = generally_page[0]['name']

    try:
        obj_response = requests.get(generally_name, timeout=5)
        obj_response.raise_for_status()
    except RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_page', id=generally_id))

    parser_status_code = obj_response.status_code
    h1_tag, title_tag, meta_tag = fill_answer(generally_name)

    check_site(generally_id, parser_status_code, h1_tag, title_tag, meta_tag)

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_page', id=generally_id))


if __name__ == '__main__':
    app.run(debug=True)
