from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


app.config.from_object("app.config.Config")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://camp_ec_master:FYbpTtwBA0xve4dkHdKE@camp-ec-db-001.cahamprlbrto.us-east-2.rds.amazonaws.com:5432/camp_ec_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

from app.models.cards_model import Card
db.create_all()

from app import routes