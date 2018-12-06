import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = basedir + '/app/static/img/'
    UPLOADS_DEFAULT_URL = 'http://127.0.0.1:5000/static/img/'
    UPLOADED_IMAGES_DEST = basedir + '/app/static/img/'
    UPLOADED_IMAGES_URL = 'http://127.0.0.1:5000/static/img/'
