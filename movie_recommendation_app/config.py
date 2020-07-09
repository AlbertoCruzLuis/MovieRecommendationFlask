import os

class Config(object):
    SECRET_KEY = 'secret_key'

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'movie_recommendation_app/static/img/film/'
    ALLOWED_EXTENSIONS = {'jpg'}