import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    APP_SETTINGS="config.DevelopmentConfig"
    DEBUG = True

