from models import User, Organization, OrgMember, AttendanceSession, AttendanceRecord
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']

    organizations = ma.Nested('OrganizationSchema', many=True) 
    org_members = ma.Nested('OrgMemberSchema', many=True)

class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password']

    organizations = ma.Nested('OrganizationSchema', many=True, exclude=['member']) 
    org_members = ma.Nested('OrgMemberSchema', many=True)  
    attendance_sessions = ma.Nested('AttendanceSessionSchema', many=True)  
    attendance_records = ma.Nested('AttendanceRecordSchema', many=True) 

class OrganizationCreteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organization

    created_by = ma.Nested('UserSchema', only=['name', 'email', 'role'])

    
class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organization
    
    member = ma.Nested('OrgMemberSchema', many=True)
    attendance_sessions = ma.Nested('AttendanceSessionSchema', many=True) 
    created_by = ma.Nested('UserSchema', only=['name', 'email', 'role'])
    attendance_records = ma.Nested('AttendanceRecordSchema', many=True)


class OrgMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrgMember
        exclude = ['id']

    user = ma.Nested('UserSchema', only=['name', 'email', 'role', 'id'])
    
class AttendanceSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceSession

    created_by = ma.Nested('UserSchema', only=['name'])
    organization = ma.Nested('OrganizationSchema', only=['name'])
    

class AttendanceRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceRecord

    user = ma.Nested('UserSchema', only=['name', 'email'])
    attendance_session = ma.Nested('AttendanceSessionSchema', only=['date', 'time_open', 'time_close'])


user_login_schema = UserLoginSchema()
user_register_schema = UserRegisterSchema()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

organization_create_schema = OrganizationCreteSchema()

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)

org_member_schema = OrgMemberSchema()
org_members_schema = OrgMemberSchema(many=True)

attendance_session_schema = AttendanceSessionSchema()
attendance_sessions_schema = AttendanceSessionSchema(many=True)

attendance_record_schema = AttendanceRecordSchema()
attendance_records_schema = AttendanceRecordSchema(many=True)
