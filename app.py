from flask import Flask, jsonify, request
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import db, User , Organization, OrgMember, AttendanceSession, AttendanceRecord
from schema import user_login_schema, user_register_schema ,user_schema, users_schema, organization_create_schema ,organizations_schema, organization_schema,org_member_schema, org_members_schema, attendance_session_schema, attendance_sessions_schema, attendance_record_schema, attendance_records_schema
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
app.config.from_object(Config)
CORS(app)

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
        result = user_register_schema.dump(new_user)
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
    result = user_login_schema.dump(user)

    if user and check_password_hash(user.password, password):
        return jsonify({
            'status': 'success',
            'data': result,
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

# Endpoint menambahkan organisasi
@app.route('/api/organizations', methods=['POST'])
def create_organization():
    data = request.get_json()
    name = data.get('name')
    enroll_code = data.get('enroll_code')
    user_id = data.get('user_id')

    if Organization.query.filter_by(name=name).first():
        return jsonify({
            'status': 'conflict',
            'message': 'Organization already exists'
        }), 409

    try:
        user = User.query.get_or_404(user_id)
        user.role = 'pelatih'
        db.session.commit()
        # Tambahkan organisasi
        organization = Organization(name=name, enroll_code=enroll_code, user_id=user_id)
        db.session.add(organization)
        db.session.flush()  # Memastikan ID organisasi dihasilkan

        # Tambahkan pelatih sebagai anggota
        new_member = OrgMember(org_id=organization.id, user_id=user_id)
        db.session.add(new_member)

        db.session.commit()

        result = organization_create_schema.dump(organization)
        return jsonify({
            'status': 'success',
            'data': result,
            'message': 'Organization created successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

    
# Endpoint menampilkan semua data Organization
@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    org = Organization.query.all()
    if not org:
        return jsonify({
            'status': 'not found',
            'message': 'organization not found',
            'data': []
        })
    
    result = organizations_schema.dump(org)
    return jsonify({
        'status': 'success',
        'data': result,
        'message': 'organizations found'
    })

# Endpoint menampilkan satu data Organization berdasarkan ID
@app.route('/api/organizations/<int:id>', methods=['GET'])
def get_organization(id):
    try:
        org = Organization.query.get_or_404(id)
        result = organization_schema.dump(org)
        return jsonify({
            'status': 'success',
            'data': result,
            'message': 'organization found'
        }), 200
    
    except Exception as e:
        return jsonify({    
            'status': 'error',
            'message': str(e)
        })

# Endpoint update data Organization berdasarkan ID
@app.route('/api/organizations/<int:id>', methods=['PUT'])
def update_organization(id):
    org = Organization.query.get_or_404(id)
    data = request.get_json()

    for field in ['name', 'enroll_code', 'created_by']:
        if field in data:
            setattr(org, field, data[field])

    db.session.commit()
    result = organization_schema.dump(org)

    return jsonify({
        'status': 'success',
        'data': result,
        'message': 'organization updated successfully'
    })

# Endpoint menghapus data Organization berdasarkan id
@app.route('/api/organizations/<int:id>', methods=['DELETE'])
def delete_organization(id):
    org = Organization.query.get_or_404(id)

    if not org:
        return jsonify({
            'status': 'error',
            'message': 'Organization not found'
        }), 400
    
    db.session.delete(org)
    db.session.commit()

    return jsonify({    
        'status': 'success',
        'message': 'organization deleted successfully'
    })


# Endpoint gabung Organization dan User
@app.route('/api/join-organization', methods=['POST'])
def join_organization():
    data = request.json
    
    # Ambil user_id dari token atau request
    user_id = data.get('user_id')  # Di sistem real, ini harus dari token autentikasi
    enroll_code = data.get('enroll_code')
    
    if not user_id or not enroll_code:
        return jsonify({'error': 'User ID and enroll code are required.'}), 400

    try:
        # Validasi organisasi berdasarkan enroll_code
        organization = Organization.query.filter_by(enroll_code=enroll_code).first()
        if not organization:
            return jsonify({'error': 'Invalid enroll code.'}), 404
        
        # Cek apakah user sudah menjadi anggota organisasi
        existing_member = OrgMember.query.filter_by(org_id=organization.id, user_id=user_id).first()
        if existing_member:
            return jsonify({'error': 'User is already a member of this organization.'}), 400
        
        # Tambahkan ke tabel OrgMember
        new_member = OrgMember(org_id=organization.id, user_id=user_id)
        db.session.add(new_member)
        db.session.commit()

        return jsonify({'message': 'Successfully joined the organization.'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)