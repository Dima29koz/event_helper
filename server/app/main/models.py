from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from server.app import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


person_to_event = db.Table(
    'person_to_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('member_id', db.Integer, db.ForeignKey('event_member.id')),
)

product_to_event = db.Table(
    'product_to_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
)


class User(db.Model, UserMixin):
    def __init__(self, username: str, email: str, pwd: str):
        self.username = username
        self.email = email
        self.pwd = generate_password_hash(pwd)
        self.add()

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12))
    contacts = db.Column(db.String(100))
    is_email_verified = db.Column(db.Boolean, default=False)
    pwd = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.username

    def check_password(self, password: str):
        """
        Verified users password.

        :param password: user password
        :type password: str
        :return: result of verification
        :rtype: bool
        """
        return check_password_hash(self.pwd, password)

    def add(self):
        """added user to DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def set_email(self, new_email: str):
        self.email = new_email
        self.is_email_verified = False
        db.session.commit()

    def set_name(self, new_name: str):
        self.username = new_name
        db.session.commit()

    def set_pwd(self, new_pwd: str):
        self.pwd = generate_password_hash(new_pwd)
        db.session.commit()

    def verify_email(self):
        self.is_email_verified = True
        db.session.commit()

    def get_token(self, token_type: str, expires_in=600):
        return jwt.encode(
            {token_type: self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_token(token: str, token_type: str):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])[token_type]
        except Exception as _:
            return
        return get_user_by_id(user_id)


def get_user_by_id(user_id: int) -> User | None:
    """returns user by id if user exists"""
    return User.query.filter_by(id=user_id).first()


class Role(db.Model):
    def __init__(self, name):
        self.name = name
        self.add()

    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def __repr__(self):
        return self.name


class EventMember(db.Model):
    __tablename__ = 'event_member'
    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.String(50), nullable=False)
    days_amount = db.Column(db.Integer(), nullable=False)
    is_drinker = db.Column(db.Boolean, default=False)
    money_impact = db.Column(db.Float())
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def __repr__(self):
        return self.nickname


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.UnicodeText)
    location_id = db.Column(db.Integer(), db.ForeignKey('location.id'), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    cost_reduction_factor = db.Column(db.Integer, default=25, nullable=False)

    def __repr__(self):
        return self.title


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    geo = db.Column(db.String(100), nullable=False)
    maps_link = db.Column(db.String(100), nullable=False)
    description = db.Column(db.UnicodeText)

    def __repr__(self):
        return self.address


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class ProductType(db.Model):
    __tablename__ = 'product_type'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class ProductUnit(db.Model):
    __tablename__ = 'product_unit'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class ProductState(db.Model):
    __tablename__ = 'product_state'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class BaseProduct(db.Model):
    __tablename__ = 'base_product'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('product_category.id'), nullable=False)
    type_id = db.Column(db.Integer(), db.ForeignKey('product_type.id'), nullable=False)
    unit_id = db.Column(db.Integer(), db.ForeignKey('product_unit.id'), nullable=False)
    price_supposed = db.Column(db.Float())

    def __repr__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('base_product.id'), nullable=False)
    state_id = db.Column(db.Integer(), db.ForeignKey('product_state.id'), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    price_final = db.Column(db.Float())
    description = db.Column(db.UnicodeText)
    market = db.Column(db.String(50))

    def __repr__(self):
        return self.id
