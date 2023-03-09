import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def add_data(url):
    connection = get_conn()
    cursor = connection.cursor()

    insert_table = f'''INSERT INTO url (name, created_at) VALUES ('{url}', now())
    RETURNING id'''
    cursor.execute(insert_table)
    id_of_new_row = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return id_of_new_row


def add_side():
    connection = get_conn()
    cursor = connection.cursor()

    get_data = f'''SELECT * FROM url ORDER BY id DESC;'''
    cursor.execute(get_data)

    data = cursor.fetchall()
    urls = list()
    for all in data:
        urls.append({'id': all[0], 'name': all[1], 'created_at': all[2]})

    cursor.close()
    connection.close()

    return urls


def check_identity(url):
    connection = get_conn()
    cursor = connection.cursor()

    check_url = f'''SELECT EXISTS (SELECT * FROM url WHERE name = '{url}');'''
    cursor.execute(check_url)
    answer = cursor.fetchall()

    if answer[0][0]:
        url_for_db = f'''SELECT * FROM url WHERE name = '{url}';'''
        cursor.execute(url_for_db)
        data = cursor.fetchall()
        page = list()
        for all in data:
            page.append({'id': all[0], 'name': all[1], 'created_at': all[2]})

        cursor.close()
        connection.close()
        return page

    else:
        cursor.close()
        connection.close()

        return False


def show_page(id):
    connection = get_conn()
    cursor = connection.cursor()

    get_last_page = f'''SELECT * FROM url WHERE id = '{id}';'''
    cursor.execute(get_last_page)

    data = cursor.fetchall()
    page = list()
    for all in data:
        page.append({'id': all[0], 'name': all[1], 'created_at': all[2]})

    cursor.close()
    connection.close()

    return page


def check_site(id_from_url_table):
    connection = get_conn()
    cursor = connection.cursor()

    insert_table = f'''INSERT INTO url_checks (url_id, created_at) VALUES ('{id_from_url_table}', now())
    RETURNING id'''
    cursor.execute(insert_table)

    id_of_new_row = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return id_of_new_row


def show_page_checks(id):
    connection = get_conn()
    cursor = connection.cursor()

    page = f'''SELECT * FROM url_checks WHERE url_id = '{id}';'''
    cursor.execute(page)

    data = cursor.fetchall()
    page = list()
    for all in data:
        page.append({'id': all[0], 'url_id': all[1], 'status_code': all[2], 'h1': all[3],
                     'title': all[4], 'description': all[5], 'created_at': all[6]})

    cursor.close()
    connection.close()

    return page

