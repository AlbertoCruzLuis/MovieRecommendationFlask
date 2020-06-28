import os

class Config(object):
    SECRET_KEY = 'secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/movie_recomendation'