import os
from utils.converters import str_to_bool
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = str_to_bool(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CORS_HEADERS = os.getenv("CORS_HEADERS")
    S3_BUCKET                 = os.getenv("S3_BUCKET_NAME")
    S3_KEY                    = os.getenv("S3_ACCESS_KEY")
    S3_SECRET                 = os.getenv("S3_SECRET_ACCESS_KEY")
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)