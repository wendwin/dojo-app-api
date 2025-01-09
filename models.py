from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False,  default='atlet')

    organizations = db.relationship('Organization', backref='created_by', lazy=True)    
    org_members = db.relationship('OrgMember', backref='user', lazy=True)
    attendance_sessions = db.relationship('AttendanceSession', backref='created_by', lazy=True)
    attendance_records = db.relationship('AttendanceRecord', backref='user', lazy=True)

# Model Organization
class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enroll_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    member = db.relationship('OrgMember', backref='organization', lazy=True,  cascade="all, delete-orphan")
    attendance_sessions = db.relationship('AttendanceSession', backref='organization', lazy=True)
    attendance_records = db.relationship(
    'AttendanceRecord',
    secondary='attendance_sessions',  # Hubungkan melalui AttendanceSession
    primaryjoin='Organization.id == AttendanceSession.org_id',  # Relasi Organization ke AttendanceSession
    secondaryjoin='AttendanceSession.id == AttendanceRecord.attendance_session_id',  # Relasi AttendanceSession ke AttendanceRecord
    lazy=True,
    viewonly=True  # Menghindari modifikasi langsung
)

    
# Model OrgMember
class OrgMember(db.Model):
    __tablename__ = 'org_members'

    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

# Model AttendanceSession
class AttendanceSession(db.Model):
    __tablename__ = 'attendance_sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='open', nullable=False)
    time_open = db.Column(db.Time, nullable=False)
    time_close = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

    attendance_records = db.relationship('AttendanceRecord', backref='attendance_session', lazy=True)
    

# Model AttendanceRecord
class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    attendance_session_id = db.Column(db.Integer, db.ForeignKey('attendance_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False) 
