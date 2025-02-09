from flask import Blueprint, render_template, redirect, session, request
from models import db, Cart, Item

cart_bp = Blueprint('cart', __name__)

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
    if session.get('user_id') is None:
        return redirect('/')

    code = request.args.get('code')
    user_id = session['user_id']

    product = Item.query.filter_by(code=int(code)).first()
    cart_item = Cart.query.filter_by(user_id=user_id, item_id=product.id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=user_id, item_id=product.id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()
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
