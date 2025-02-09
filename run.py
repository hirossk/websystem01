from app import app
from models import db

with app.app_context():
    db.create_all()  # 初回実行時にDBを作成

app.run(debug=True)
