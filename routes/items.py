from flask import Blueprint, render_template, session, redirect,request
from models import Item

items_bp = Blueprint('items', __name__)

@items_bp.route('/list')
def list():
    if session.get('user_id') is None:
        return redirect('/auth/')
    
    # データベースから全てのアイテムを取得
    items = Item.query.all()
    return render_template('itemlist.html', items=items, user_name=session.get('user_name', ''))

@items_bp.route('/detail')
def detail():
    if session.get('user_id') is None:
        return redirect('/auth/')
    
    # リクエストから商品コードを取得
    code = request.args.get('code')
    
    # データベースから商品コードに一致するアイテムを取得
    product = Item.query.filter_by(code=int(code)).first()
    
    return render_template('detail.html', product=product)

# field検索
# items = Item.query.filter_by(field='').all()
# カテゴリーAへの追加を記載する