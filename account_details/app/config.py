from os import getenv
from utils.converters import str_to_bool
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = str_to_bool(getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    CORS_HEADERS = getenv("CORS_HEADERS")
    S3_BUCKET                 = getenv("S3_BUCKET_NAME")
    S3_KEY                    = getenv("S3_ACCESS_KEY")
    S3_SECRET                 = getenv("S3_SECRET_ACCESS_KEY")
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)