import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify, render_template
from flask_jwt import JWT, jwt_required, current_identity


class UserInfo(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def create_user_table():
    with sqlite3.connect("point_sale.db") as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user_info(user_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'full_name TEXT NOT NULL,'
                       'username TEXT NOT NULL,'
                       'password TEXT NOT NULL)')
        print('User Table Created')


def create_product_table():
    connection = sqlite3.connect('point_sale.db')

    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS product_info(product_id INTEGER PRIMARY KEY AUTOINCREMENT'
                   'category TEXT NOT NULL,'
                   'name TEXT NOT NULL,'
                   'price TEXT NOT NULL,'
                   'description TEXT NOT NULL)')
    print('Product Table Created')
    connection.close()


create_user_table()
create_product_table()


app = Flask(__name__)
app.debug = True


@app.route('/registration/', methods=['POST'])
def register_user():
    response = {}

    if request.method == "POST":
        full_name = request.form['full_name']
        username = request. form['username']
        password = request.form['password']

        with sqlite3.connect('point_sale.db') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO user_info('
                           "full_name,"
                           "username,"
                           "password) VALUES(?, ?, ?)", (full_name, username, password))
            connection.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response

@app.route('/login/')
def user_login():
    pass

@app.route('/adding/', methods=['POST'])
def add_products():
