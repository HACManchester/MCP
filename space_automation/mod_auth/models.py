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
    display_name = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    password = CharField()
    email = CharField(unique=True)
    membership_amount = IntegerField(null=True)

    @classmethod
    def create_user(cls, username, display_name, first_name, last_name, password, email, membership_amount):
        try:
            with db.transaction():
                cls.create(
                    username=username,
                    display_name=display_name,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    email=email,
                    membership_amount=membership_amount
                )
        except IntegrityError:
            raise ValueError("username and email must be unique")


class ContactDeets(Base):
    username = ForeignKeyField(
        rel_model=User,
        related_name='address'
    ),
    address1 = CharField()
    address2 = CharField()
    address3 = CharField()
    postcode = CharField()
    phone_num = IntegerField()


class EmergencyContact(Base):
    username = ForeignKeyField(
        rel_model=User,
        related_name='emergency_contact'
    )
    who = CharField()
    how = TextField()
    other_info = TextField()


def initialise():
    db.connect()
    db.create_tables([User], safe=True)
    db.close()
