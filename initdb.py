from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    item = db.relationship('Item', backref=db.backref('carts', lazy=True))

# Check if the database file exists in the instance folder, and delete it if it does.
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'site.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Existing database '{db_path}' deleted.")
else:
    print(f"Database '{db_path}' does not exist.")

# Recreate the database tables.
with app.app_context():
    db.create_all()
    users = [
        {'email': 'user1@example.com', 'password': 'password1'},
        {'email': 'user2@example.com', 'password': 'password2'},
        {'email': 'user3@example.com', 'password': 'password3'}
    ]

    for user_data in users:
        hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
        user = User(email=user_data['email'], password=hashed_password)
        db.session.add(user)
    print("Database tables recreated.")

    items = [
        {'code': 1001, 'name': '商品A', 'overview': '商品の概要A', 'price': 1000, 'category': 'カテゴリーA'},
        {'code': 1002, 'name': '商品B', 'overview': '商品の概要B', 'price': 2000, 'category': 'カテゴリーB'},
        {'code': 1003, 'name': '商品C', 'overview': '商品の概要C', 'price': 3000, 'category': 'カテゴリーA'},
        {'code': 1004, 'name': '商品D', 'overview': '商品の概要D', 'price': 4000, 'category': 'カテゴリーC'},
        {'code': 1005, 'name': '商品E', 'overview': '商品の概要E', 'price': 5000, 'category': 'カテゴリーB'}
    ]

    for item_data in items:
        item = Item(**item_data)
        db.session.add(item)

    carts = [
      {'user_id': 1, 'item_id': 1, 'quantity': 2},
      {'user_id': 1, 'item_id': 3, 'quantity': 1},
      {'user_id': 2, 'item_id': 2, 'quantity': 3},
    ]

    for cart_data in carts:
        cart = Cart(**cart_data)
        db.session.add(cart)

    db.session.commit()
