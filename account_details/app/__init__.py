from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
cors = CORS(app)


app.config.from_object("app.config.Config")


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes