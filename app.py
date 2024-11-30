from flask import Flask, jsonify, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import db, User , user_schema, users_schema
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# @app.route('/',methods=['GET','POST'])
# def home():
#     if request.method=='POST':
#         return render_template('index.html')
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)