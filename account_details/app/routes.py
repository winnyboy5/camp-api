import os
from app import app
from app.api import API
from flask import request, jsonify

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify(
        logged_in_as=current_user, 
        username=claims['username'],
        email=claims['email'],
        mobile=claims['mobile'],
        country=claims['country'],
        created_at=claims['created_at'],
        updated_at=claims['updated_at']
    ), 200