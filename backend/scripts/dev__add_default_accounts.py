"""Script for populating dev database with default user accounts."""
from sqlalchemy import exists
from werkzeug.security import generate_password_hash

from medtagger.database import db_session
from medtagger.database.models import User, Role


def insert_admin_account() -> None:
    """Insert default admin account."""
    with db_session() as session:
        user_email = 'admin@medtagger.com'
        user_exists = session.query(exists().where(User.email == user_email)).scalar()
        if user_exists:
            print('Admin user already exists with email "{}"'.format(user_email))
            return
        password = 'medtagger1'
        password_hash = generate_password_hash(password)
        user = User(user_email, password_hash, 'Admin', 'Medtagger')
        role = Role.query.filter_by(name='admin').first()
        user.roles.append(role)
        session.add(user)
        print('User added with email "{}" and password "{}"'.format(user_email, password))


if __name__ == '__main__':
    insert_admin_account()