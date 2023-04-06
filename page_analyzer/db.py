import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def add_data(connection, url):
    with connection.cursor() as cursor:
        insert_table = '''INSERT INTO urls (name, created_at) VALUES (%s, now())
        RETURNING id'''
        cursor.execute(insert_table, (url,))
        id_of_new_row = cursor.fetchone()[0]
        connection.commit()
        return id_of_new_row


def get_all_pages(connection):
    with connection.cursor() as cursor:
        get_data = '''SELECT * FROM (
            SELECT
                DISTINCT ON (urls.name)
                urls.id,
                urls.name,
                url_checks.status_code,
                url_checks.created_at AS created_at_url_checks
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.name, created_at_url_checks DESC
            ) AS MYTable
            ORDER BY MYTable.id DESC;'''
        cursor.execute(get_data)
        data = cursor.fetchall()
        urls = list()
        for all in data:
            urls.append({'id': all[0], 'name': all[1], 'status_code': all[2], 'created_at': all[3]})
        return urls


def check_identity(connection, url):
    with connection.cursor() as cursor:
        check_url = '''SELECT EXISTS (SELECT * FROM urls WHERE name = %s);'''
        cursor.execute(check_url, (url,))
        answer = cursor.fetchall()

        if answer[0][0]:
            url_for_db = '''SELECT * FROM urls WHERE name = %s;'''
            cursor.execute(url_for_db, (url,))
            data = cursor.fetchall()
            page = dict()
            for all in data:
                page.update({'id': all[0], 'name': all[1], 'created_at': all[2]})
            return page

        return None


def get_page(connection, id):
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM urls WHERE id = %s',
            (id,)
        )
        data = cursor.fetchall()
        page = list()
        for all in data:
            page.append({'id': all[0], 'name': all[1], 'created_at': all[2]})
        return page


def add_check_info(connection, id_from_url_table, status_code, h1, title, meta):
    with connection.cursor() as cursor:
        insert_table = '''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s, %s, %s, now())
        RETURNING id'''
        cursor.execute(insert_table, (id_from_url_table, status_code, h1, title, meta,))
        id_of_new_row = cursor.fetchone()[0]
        connection.commit()
        return id_of_new_row


def get_page_after_checking(connection, id):
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s',
            (id,)
        )
        data = cursor.fetchall()
        page = list()
        for all in data:
            page.append({'id': all[0], 'url_id': all[1], 'status_code': all[2], 'h1': all[3],
                         'title': all[4], 'description': all[5], 'created_at': all[6]})
        return page
