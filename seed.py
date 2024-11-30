from app import app,db
from models import User, Organization
from werkzeug.security import generate_password_hash

def seed_users():
    with app.app_context():
        users = [
            User(
                id=1,
                name='Budi Santoso',
                email='budi@gmail.com',
                password=generate_password_hash('budi1'),
                role='pelatih'
            ),
            User(
                id=2,
                name='Cindy Amalia',
                email='cindy@gmail.com',
                password=generate_password_hash('cindi2'),
                role='atlet'
            ),
            User(
                id=3,
                name='Dimas Aditya',
                email='dimas@gmail.com',
                password=generate_password_hash('dimas3'),
                role='atlet'
            ),
        ]

        db.session.add_all(users)
        db.session.commit()

        print("Seeding data User berhasil.")

def seed_organizations():
    with app.app_context():
        organizations = [
            Organization(
                id=1,
                name='Kota Yogyakarta',
                enroll_code='A1-YK-001',
                created_by=1
            ),
        ]

        db.session.add_all(organizations)
        db.session.commit()

        print("Seeding data Organization berhasil.")


if __name__ == '__main__':
    seed_users()
    seed_organizations()
