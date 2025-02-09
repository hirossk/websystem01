from flask import Blueprint, render_template, session, redirect
from models import Item

items_bp = Blueprint('items', __name__)

@items_bp.route('/list')
def list():
    if session.get('user_id') is None:
        return redirect('/auth/')
    
    items = Item.query.all()
    return render_template('itemlist.html', items=items, user_name=session.get('user_name', ''))
