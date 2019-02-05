import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from flask.ext.bcrypt import check_password_hash
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    bio = TextField(default='')

    class Meta:
        database = DATABASE
        # default sorting in peewee meta class
        # '-' in the first of field name in order_by section, peewee perform DESC ordering of filed.
        # trailing comma if there's only one tuple member.
        # You can use list, order_by = ['-joined_at']
        order_by = ('-joined_at',)

    # classmethod is a method that belongs to a class that can create the class it belongs to
    # the way it works, if we don't have classmethod we have to create a user instance to call create user which will create a user instance
    # classmethod is agreat solution to building classes from nothing
    @classmethod
    def create_user(cls, username, email, password, admin=False, bio=''):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin,
                bio=bio
            )
        except IntegrityError:
            raise ValueError("User already exists!")


def initiatize():
    DATABASE.connect()
    DATABASE.create_table([User], safe=True)
    DATABASE.close()
