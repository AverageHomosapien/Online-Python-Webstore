import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'pbkdf2:sha256:5613952$vT9fkZM8$04dfa35c6476acf7e788a1b5b3c35e217c78dc04539d295f011f01f18cd2175f'
    #APPLICATION_ROOT = 'sqlite:///' + os.path.join(basedir, 'app')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMG_FOLDER = os.path.join('static', 'img')
    ITEM_FOLDER = os.path.join(IMG_FOLDER, 'items')
