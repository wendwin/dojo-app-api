from app import app,db
from models import User, Organization
from werkzeug.security import generate_password_hash

def seed_users():
    with app.app_context():
        users = [
            User(
                id=1,
                name='Andi Perkasa',
                email='andiperkasa@gmail.com',
                password=generate_password_hash('andi123'),
                role='atlet'
            ),
            User(
                id=2,
                name='Budi Santoso',
                email='budisantoso@gmail.com',
                password=generate_password_hash('budi123'),
                role='atlet'
            ),
            User(
                id=3,
                name='Heru Gunawan',
                email='herugunawan@gmail.com',
                password=generate_password_hash('heru123'),
                role='atlet'
            ),
            User(
                id=4,
                name='Fajar Kurniawan',
                email='fajarkurniawan@gmail.com',
                password=generate_password_hash('fajar123'),
                role='atlet'
            ),
            User(
                id=5,
                name='Dika Bayu',
                email='dikabayu5@gmail.com',
                password=generate_password_hash('dika123'),
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
                name='orgs1',
                enroll_code='orgs1',
                created_by=1
            ),
            Organization(
                id=2,
                name='orgs2',
                enroll_code='orgs2',
                created_by=2
            ),
            Organization(
                id=3,
                name='orgs3',
                enroll_code='orgs3',
                created_by=3
            ),
        ]

        db.session.add_all(organizations)
        db.session.commit()

        print("Seeding data Organization berhasil.")


if __name__ == '__main__':
    seed_users()
    # seed_organizations()
