from flask import Flask, redirect, render_template
from models import db
from routes import auth_bp, cart_bp, items_bp, users_bp

# from google.colab import output

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

# Blueprint登録
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(items_bp, url_prefix='/items')
app.register_blueprint(users_bp, url_prefix='/users')

@app.route('/')
def logout():
    return redirect('/auth/')
    # return render_template('top.html')    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
