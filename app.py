from flask import Flask
from models import db
from routes import auth_bp, cart_bp, items_bp
import os
from pyngrok import ngrok
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

# Blueprint登録
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(items_bp, url_prefix='/items')

# Google Colab やリモート環境で ngrok を使用
if 'COLAB_GPU' in os.environ:
    ngrok.kill()  # 既存の ngrok プロセスを停止
    public_url = ngrok.connect(5000)  # ngrokトンネルを開く
    print(f"ngrok URL: {public_url}")
    run_with_ngrok(app)

if __name__ == '__main__':
    app.run()
