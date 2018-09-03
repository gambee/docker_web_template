import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST')
    UPLOADS_DEFAULT_URL = os.environ.get('UPLOADS_DEFAULT_URL')
    UPLOADED_DDUMPS_DEST = os.environ.get('UPLOADED_DDUMPS_DEST')
    UPLOADED_DDUMPS_URL = os.environ.get('UPLOADED_DDUMPS_URL')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
