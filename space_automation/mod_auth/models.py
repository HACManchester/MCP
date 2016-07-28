# database should be defined in config.py, as it's wrong I'm temporarily
# creating a db here so I can check my work
# from space_automation import db
from peewee import *
from flask_bcrypt import generate_password_hash

# this is for inital testing purposes only and should be removed as soon as the proper
# db is in place.
DB = 'temp.db'
db = SqliteDatabase(DB)


class Base(Model):
    class Meta:
        db = db


class User(Base):
    username = CharField(unique=True)
    display_name = CharField()
    password = CharField()
    email = CharField(unique=True)

    @classmethod
    def create_user(cls, username, display_name, password, email):
        try:
            with db.transaction():
                cls.create(
                    username=username,
                    display_name=display_name,
                    password=generate_password_hash(password),
                    email=email
                )
        except IntegrityError:
            raise ValueError("username and email must be unique")


def initialise():
    db.connect()
    db.create_tables([User], safe=True)
    db.close()
