from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, default = datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = self.__create_password(password)

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Film(db.Model):

    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(70), nullable=False)
    image_name = db.Column(db.String(70), unique=True, nullable=False)


    def __init__(self, title, year, image_name):
        self.title = title
        self.year = year
        self.image_name = image_name
