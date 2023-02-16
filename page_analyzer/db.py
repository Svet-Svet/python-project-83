import psycopg2
import os


DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def add_data(url):
    connection = get_conn()
    cursor = connection.cursor()

    insert_table = f'''INSERT INTO urls (name, created_at) VALUES ('{url}', now())'''
    cursor.execute(insert_table)
    connection.commit()
    cursor.close()
    connection.close()


def add_side():
    connection = get_conn()
    cursor = connection.cursor()

    get_data = f'''SELECT * FROM urls'''
    cursor.execute(get_data)

    data = cursor.fetchall()
    urls = list()
    for all in data:
        urls.append({'id': all[0], 'name': all[1], 'created_at': all[2]})

    return urls

