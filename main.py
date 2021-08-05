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
    cursor.execute('CREATE TABLE IF NOT EXISTS product_info(product_id INTEGER PRIMARY KEY AUTOINCREMENT,'
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


@app.route('/adding/', methods=['POST'])
def add_products():
    response = {}

    if request.method == "POST":
        category = request.form['category']
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        with sqlite3.connect("point_sale.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO product_info("
                           "category"
                           "name"
                           "price"
                           "description VALUES(?, ?, ?, ?", (category, name, price, description))
            connection.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response


@app.route('/viewing/')
def view_products():
    response = {}

    with sqlite3.connect("point_sale.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product_info")

        posts = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = posts
    return response


@app.route('/updating/<int:product_id>', methods=["POSTS"])
def updating_products(product_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('point_sale.db') as conn:
            incoming_data = dict(request.json)
            put_data = {}

            if incoming_data.get("category") is not None:
                put_data["category"] = incoming_data.get("category")
                with sqlite3.connect('point_sale.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product_info SET category =?", (put_data["category"], product_id))
                    conn.commit()
                    response['message'] = "Update was Successful"
                    response['status_code'] = 200

            elif incoming_data.get("name") is not None:
                put_data["name"] = incoming_data.get("name")

                with sqlite3.connect('point_sale.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product_info SET name =?", (put_data["name"], product_id))
                    conn.commit()
                    response['message'] = "Update was Successful"
                    response['status_code'] = 200

            elif incoming_data.get("price") is not None:
                put_data['price'] = incoming_data.get('price')

                with sqlite3.connect('point_sale.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product_info SET price =? WHERE id=?", (put_data["price"], product_id))
                    conn.commit()

                    response["price"] = "Price updated successfully"
                    response["status_code"] = 200

            elif incoming_data.get("description") is not None:
                put_data['description'] = incoming_data.get('description')

                with sqlite3.connect('point_sale.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product_info SET description =? WHERE id=?", (put_data["description"], product_id))
                    conn.commit()

                    response["description"] = "Description updated successfully"
                    response["status_code"] = 200
    return response


@app.route('/deleting/<int:item_id>')
def delete_products(item_id):
    pass


if __name__ == '__main__':
    app.run()
    app.debug = True
