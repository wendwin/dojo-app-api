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

# Endpoint registrasi
@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    
    if not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({
            'error': 'missing required fields: name, email or password'
            }), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({
            'status': 'error',
            'message': 'email already used'
        }), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
        return jsonify({
            'status': 'success',
            'data': result,
            'message': 'user registered successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Endpoint login 
@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify({
            'status': 'success',
            'data': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            },
            'message': 'user logged in successfully'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'invalid email or password'
        }), 401   

# Endpoint menampilkan semua data User
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify({
            'status': 'not found',
            'message': 'user not found',
            'data': []
        })

    result = users_schema.dump(users)
    return jsonify({
        'status': 'success',
        'data': result,
        'message': 'users found'
    })

# Endpoint menampilkan satu data User berdasarkan ID
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get_or_404(id)
        result = user_schema.dump(user)
        return jsonify({
            'status': 'success',
            'data': result,
            'message': 'user found'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 404

# Endpoint update data User berdasarkan ID
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() 

    for field in ['nama', 'email', 'password', 'tanggal_lahir', 'alamat', 'no_telepon', 'jenis_kelamin', 'role']:
        if field in data:
            setattr(user, field, generate_password_hash(data[field]) if field == 'password' else data[field])

    db.session.commit()
    result = user_schema.dump(user)

    return jsonify({
        'status': 'success',
        'data': result,
        'message': 'user updated successfully'
    }), 200

# Endpoint menghapus data user berdasarkan id
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)

    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 400
    
    db.session.delete(user)
    db.session.commit()

    # user_delete = user_schema.dump(user)
    return jsonify({
        'status': 'success',
        'message': 'user deleted successfully'
    })  


if __name__ == '__main__':
    app.run(debug=True)