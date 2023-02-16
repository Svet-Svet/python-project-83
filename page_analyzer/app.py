from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from validators import url

from page_analyzer.db import add_data, add_side

app = Flask(__name__)
app.config.update(
    SECRET_KEY='123456'
)

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template(
#         '404.html'
#     ), 404


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('urls/<id>')
# def get_urls_id():
#     pass


@app.route('/urls', methods=['POST', 'GET'])
def get_urls():
    if request.method == 'POST':
        url_name = request.form['url']

        if url(url_name):
            add_data(url_name)
            return redirect('/urls')
        else:
            flash('Некорректный URL', 'error')
            return redirect(url_for('index'))
    else:
        return render_template('urls.html', urls=add_side())


if __name__ == '__main__':
    app.run(debug=True)

