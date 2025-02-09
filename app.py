from flask import Flask, redirect
from models import db
from routes import auth_bp, cart_bp, items_bp
import os
from pyngrok import ngrok
from flask_ngrok import run_with_ngrok

# from google.colab import output

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

# Blueprint登録
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(items_bp, url_prefix='/items')

@app.route('/')
def logout():
    return redirect('/auth/')

# Google Colab やリモート環境で ngrok を使用
if 'COLAB_GPU' in os.environ:
    from google.colab import output

    from threading import Thread
    PORT=5000
    thread = Thread(target=lambda: app.run(port=PORT, debug=True, use_reloader=False))
    thread.start()
    output.serve_kernel_port_as_window(PORT)
    # ngrok.kill()  # 既存の ngrok プロセスを停止
    # public_url = ngrok.connect(5000)  # ngrokトンネルを開く
    # print(f"ngrok URL: {public_url}")
    # run_with_ngrok(app)
elif __name__ == '__main__':
    app.run()
