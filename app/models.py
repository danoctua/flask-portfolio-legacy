import datetime
import re
from hashlib import md5
from urllib.parse import urlencode
from contextlib import contextmanager
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from app import app
from flask_login import UserMixin
from time import time
import jwt
from flask_babel import _, get_locale, force_locale
from flask import url_for

from sqlalchemy.ext.hybrid import hybrid_property
from string import ascii_letters, digits
import random
import pycountry
import urllib


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


@contextmanager
def session_handler():
    session = db.session
    try:
        session.flush()
        yield session
        session.commit()
    except Exception as exp:
        app.logger.error(exp)
        print(exp)
        session.rollback()
        raise exp


class User(UserMixin, db.Model):
    __tablename__ = "user"

    user_id = db.Column("user_id", db.Integer, autoincrement=True, primary_key=True)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column("password", db.Text(500), nullable=True)
    name = db.Column('name', db.String(64), nullable=False)
    surname = db.Column('surname', db.String(64), nullable=False)
    gender = db.Column("gender", db.String(1), default="m")
    phone = db.Column("phone", db.String(15), nullable=True)
    telegram_u_id = db.Column("telegram_u_id", db.Integer, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.datetime(1900, 1, 1, 0, 0))
    preferred_language = db.Column("preferred_language", db.String(4), nullable=True)

    privacy = db.relationship("UserPrivacy", back_populates="user", uselist=False)
    privileges = db.relationship("UserPrivileges", back_populates="user", uselist=False)

    def __init__(self, email, password, name, surname, gender, phone,
                 approved=True):
        self.email = email
        self.password = generate_password_hash(password)
        self.name = name
        self.surname = surname
        self.gender = gender
        self.phone = phone
        self.telegram_u_id = None
        self.last_seen = datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0)
        self.approved = approved

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_reset_password_token(self, expires_in=600):
        """
        :param expires_in: time in seconds when token will expire
        :return: token in hash
        """
        return jwt.encode(
            {'reset_password': self.user_id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            tmp_dic = jwt.decode(token, app.config['SECRET_KEY'],
                                 algorithms=['HS256'])
            user_id = tmp_dic.get("reset_password")
            expired = time() > tmp_dic.get("exp", 0)
        except Exception as exp:
            return
        return User.query.get(user_id) if not expired else None

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.surname + " " + self.name

    def is_online(self):
        return self.last_seen + datetime.timedelta(minutes=3) > datetime.datetime.utcnow()


class UserPrivileges(db.Model):
    __tablename__ = "user_privileges"

    def __init__(self, user_id):
        self.user_id = user_id
        self.is_super_admin = False
        self.is_admin = False
        self.is_elder = False
        self.is_litcart = False

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.user_id",
                                                             ondelete="CASCADE", onupdate="CASCADE"), primary_key=True,
                        nullable=False)
    user = db.relationship("User", back_populates="privileges")
    is_super_admin = db.Column("is_super_admin", db.Boolean, default=False)
    is_admin = db.Column("is_admin", db.Boolean, default=False)


class UserPrivacy(db.Model):
    __tablename__ = "user_privacy"

    def __init__(self, user_id):
        self.user_id = user_id
        self.use_gravatar = False
        self.share_number = True
        self.share_email = True

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.user_id",
                                                             ondelete="CASCADE", onupdate="CASCADE"), primary_key=True,
                        nullable=False)
    user = db.relationship("User", back_populates="privacy")
    use_gravatar = db.Column("use_gravatar", db.Boolean, default=True)
    share_number = db.Column("share_number", db.Boolean, default=True)
    share_email = db.Column("share_email", db.Boolean, default=True)
