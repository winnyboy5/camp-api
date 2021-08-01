import os

from app import app
from app.api import API
from flask import request, jsonify
from flask_bcrypt import check_password_hash


from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required, 
    JWTManager,
    create_refresh_token,
    get_jwt
)

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
    refresh_token = create_refresh_token(identity=user.id, additional_claims=user.serialize())
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    claims = get_jwt()

    identity = get_jwt_identity()
    access_token = create_access_token(identity=current_user, additional_claims=claims)
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
        user_name = request.json.get("user_name", None),
        country = request.json.get("country", None),
        password = request.json.get("password", None) 
    )
    API.save_changes(newUser)
    return jsonify(
        status='saved',
    ), 200