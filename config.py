import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'webrokers made by koios on 07042017'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'flask_session:'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True

    SQLALCHEMY_POOL_SIZE = 300
    FLASKY_ADMIN = 'webrokers@yeah.net'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    DB_USERNAME = os.environ.get('DEV_DATABASE_USERNAME') or 'peter'
    DB_PASSWORD = os.environ.get('DEV_DATABASE_PASSWORD') or 'ftp123buzhidao'
    DB_HOST = os.environ.get('DEV_DATABASE_HOST') or '127.0.0.1'
    DB_DATABASE = os.environ.get('DEV_DATABASE_DATABASE') or 'r2d2'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DATABASE


class TestingConfig(Config):
    DEBUG = False
    DB_USERNAME = os.environ.get('TEST_DATABASE_USERNAME') or 'peter'
    DB_PASSWORD = os.environ.get('TEST_DATABASE_PASSWORD') or 'ftp123buzhidao'
    DB_HOST = os.environ.get('TEST_DATABASE_HOST') or '127.0.0.1'
    DB_DATABASE = os.environ.get('TEST_DATABASE_DATABASE') or 'r2d2'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DATABASE


class ProductionConfig(Config):
    DEBUG = False
    DB_USERNAME = os.environ.get('DATABASE_USERNAME') or 'peter'
    DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'ftp123buzhidao'
    DB_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'
    DB_DATABASE = os.environ.get('DATABASE_DATABASE') or 'r2d2'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DATABASE


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
