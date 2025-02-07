from flask import Flask, render_template, request, redirect
from models import db, User, Item, Cart  # models.py からインポート
import hashlib
from flask import session

app = Flask(__name__)
app.secret_key = '0000'  # セッションを使用するための秘密鍵を設定

# 初回リクエストかどうかを判定するフラグ
first_request_done = False

@app.before_request
def init_session():
    global first_request_done
    if not first_request_done:
        session['user_id'] = None
        first_request_done = True  # 2回目以降は実行しない

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)  # db を Flask アプリに紐付け

@app.route('/')
def index():
    if session['user_id'] is None:
        return render_template('login.html')
    return redirect('/list')

@app.route('/list')
def list_items():

    if session['user_id'] is None:
        return redirect('/')
    
    items = Item.query.all()
    return render_template('itemlist.html', items=items)

@app.route('/cartin')
def cartin():
    if session['user_id'] is None:
        return redirect('/')

    code = request.args.get('code')
    user_id = 1  # 仮のユーザーID、実際にはログインユーザーのIDを使用する

    product = Item.query.filter_by(code=int(code)).first()
    cart_item = Cart.query.filter_by(user_id=user_id, item_id=product.id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=user_id, item_id=product.id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()

    carts = db.session.query(Cart.quantity, Item.code, Item.name, Item.overview, Item.price).join(Item, Cart.item_id == Item.id).filter(Cart.user_id == user_id).all()
    total_price = sum(cart.quantity * cart.price for cart in carts)

    return render_template('cartitem.html', carts=carts, total_price=total_price)

@app.route('/deleteitem', methods=['POST'])
def deleteitem():
    if session['user_id'] is None:
        return redirect('/')
    
    code = request.form['code']
    user_id = 1  # 仮のユーザーID、実際にはログインユーザーのIDを使用する

    product = Item.query.filter_by(code=int(code)).first()
    if product:
        cart_item = Cart.query.filter_by(user_id=user_id, item_id=product.id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    carts = db.session.query(Cart.quantity, Item.code, Item.name, Item.overview, Item.price).join(Item, Cart.item_id == Item.id).filter(Cart.user_id == user_id).all()
    total_price = sum(cart.quantity * cart.price for cart in carts)

    return render_template('cartitem.html', carts=carts, total_price=total_price)

@app.route('/logincheck', methods=['POST'])
def logincheck():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = User.query.filter_by(email=email, password=hashed_password).first()

    if user:
        session['user_id'] = user.id
        print(user.id)
        return redirect('/list')
    else:
        return render_template('login.html', error='Invalid email or password')

@app.route('/logout')
def logout():
    session['user_id'] = None  # セッションから user_id を削除
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)