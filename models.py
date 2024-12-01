from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()

# Model User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False,  default='atlet')
    
    # Relasi
    organizations = db.relationship('Organization', backref='creator', lazy=True)
    attendance_sessions = db.relationship('AttendanceSession', backref='creator', lazy=True)
    attendance_records = db.relationship('AttendanceRecord', backref='user', lazy=True)

# Model Organization
class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enroll_code = db.Column(db.String(50), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relasi
    members = db.relationship('OrgMember', backref='organization', lazy=True)
    attendance_sessions = db.relationship('AttendanceSession', backref='organization', lazy=True)

# Model OrgMember
class OrgMember(db.Model):
    __tablename__ = 'org_members'

    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relasi
    user = db.relationship('User', backref='org_memberships')

# Model AttendanceSession
class AttendanceSession(db.Model):
    __tablename__ = 'attendance_sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    
    # Relasi
    attendance_records = db.relationship('AttendanceRecord', backref='session', lazy=True)

# Model AttendanceRecord
class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    attendance_session_id = db.Column(db.Integer, db.ForeignKey('attendance_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'hadir', 'izin', 'tidak hadir'


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']

class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organization
    # created_by = ma.auto_field()
    creator = ma.Nested('UserSchema', only=['id', 'name', 'email'])


class OrgMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrgMember

class AttendanceSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceSession


class AttendanceRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceRecord    

user_schema = UserSchema()
users_schema = UserSchema(many=True)

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)

org_member_schema = OrgMemberSchema()
org_members_schema = OrgMemberSchema(many=True)

attendance_session_schema = AttendanceSessionSchema()
attendance_sessions_schema = AttendanceSessionSchema(many=True)

attendance_record_schema = AttendanceRecordSchema()
attendance_records_schema = AttendanceRecordSchema(many=True)
