from flask import Flask, render_template
from flask import request
import hashlib

app = Flask(__name__)

items = [
    {'code': 1, 'name': 'item1', 'overview': 'This is item 1', 'price': 100, 'category': 'Category A'},
    {'code': 2, 'name': 'item2', 'overview': 'This is item 2', 'price': 200, 'category': 'Category B'},
    {'code': 3, 'name': 'item3', 'overview': 'This is item 3', 'price': 300, 'category': 'Category C'},
    {'code': 4, 'name': 'item4', 'overview': 'This is item 4', 'price': 400, 'category': 'Category D'}
]

carts = []

users = [
    {'email': 'user1@example.com', 'password': hashlib.sha256('password1'.encode()).hexdigest()},
    {'email': 'user2@example.com', 'password': hashlib.sha256('password2'.encode()).hexdigest()},
    {'email': 'user3@example.com', 'password': hashlib.sha256('password3'.encode()).hexdigest()}
]

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/list')
def list():
    return render_template('itemlist.html', items=items)

@app.route('/cartin')
def cartin():
    product_id = request.args.get('product_id')
    product = next(item for item in items if item['code'] == int(product_id))
    
    cart_item = next((cart for cart in carts if cart['code'] == product['code']), None)
    
    if cart_item:
        cart_item['quantity'] += 1
    else:
        carts.append({'code': product['code'], 'name': product['name'], 'price': product['price'], 'quantity': 1})
    
    total_price = sum(cart['price'] * cart['quantity'] for cart in carts)
    
    return render_template('cartitem.html', carts=carts, total_price=total_price)

@app.route('/deleteitem', methods=['POST'])
def deleteitem():
    product_id = request.form['product_id']
    product = next(item for item in items if item['code'] == int(product_id))
    
    cart_item = next((cart for cart in carts if cart['code'] == product['code']), None)
    
    if cart_item:
        carts.remove(cart_item)
    
    total_price = sum(cart['price'] * cart['quantity'] for cart in carts)
    
    return render_template('cartitem.html', carts=carts, total_price=total_price)

@app.route('/logincheck', methods=['POST'])
def logincheck():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = next((user for user in users if user['email'] == email and user['password'] == hashed_password), None)

    if user:
        return render_template('itemlist.html', items=items)
    else:
        return render_template('login.html', error='Invalid email or password')

if __name__ == '__main__':
    app.run(debug=True)