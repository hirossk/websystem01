from flask import Blueprint, render_template, redirect, session, request
from models import db, Cart, Item

cart_bp = Blueprint('cart', __name__)

# Cartの中身を表示する
@cart_bp.route('/view')
def viewcart():
    if session.get('user_id') is None:
        return redirect('/')
    
    user_id = session['user_id']
    user_name = session.get('user_name', '')

    carts = db.session.query(
        Cart.quantity, Item.code, Item.name, Item.overview, 
        Item.price, Item.image_path
    ).join(Item, Cart.item_id == Item.id).filter(Cart.user_id == user_id).all()

    total_price = sum(cart.quantity * cart.price for cart in carts)

    return render_template('cartitem.html', carts=carts, total_price=total_price, user_name=user_name)

@cart_bp.route('/add')
def add():
    # ユーザーがログインしているか確認
    if session.get('user_id') is None:
        return redirect('/')

    # リクエストから商品コードを取得
    code = request.args.get('code')
    user_id = session['user_id']

    # 商品コードに基づいて商品をデータベースから取得
    product = Item.query.filter_by(code=int(code)).first()
    # ユーザーのカートに同じ商品があるか確認
    cart_item = Cart.query.filter_by(user_id=user_id, item_id=product.id).first()

    # カートに商品に商品を追加処理
    
    return redirect('/cart/view')

@cart_bp.route('/delete', methods=['POST'])
def delete():
    if session.get('user_id') is None:
        return redirect('/')
    
    code = request.form['code']
    user_id = session['user_id']

    product = Item.query.filter_by(code=int(code)).first()
    if product:
        cart_item = Cart.query.filter_by(user_id=user_id, item_id=product.id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    return redirect('/cart/view')
