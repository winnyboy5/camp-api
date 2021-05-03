import os

from app import app
from app.api import API
from flask import request, jsonify
from flask_bcrypt import check_password_hash


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from app.models.user_model import User


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401
    else:
        if user.check_password(password) != True:
            return jsonify({"msg": "Bad email or password"}), 401
    

    access_token = create_access_token(identity=user.id, additional_claims=user.serialize())
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/create", methods=["POST"])
def create():
    newUser = User(
        email = request.json.get("email", None),
        mobile = request.json.get("mobile", None),
        country = request.json.get("country", None),
        password = request.json.get("password", None) 
    )
    API.save_changes(newUser)
    return jsonify(
        status='saved',
    ), 200