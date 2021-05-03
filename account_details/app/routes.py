import os
from app import app
from app.api import API
from flask import request, jsonify
from utils.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename


from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt

from app.models.account_details_model import AccountDetails

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
        user_id=claims['id'],
        email=claims['email'],
        mobile=claims['mobile'],
        country=claims['country'],
        created_at=claims['created_at'],
        updated_at=claims['updated_at']
    ), 200


@app.route("/create", methods=["POST"])
@jwt_required()
def create():
    claims = get_jwt()
    newAcc = AccountDetails(
        user_id = claims['id'],
        first_name = request.json.get("first_name", None),
        last_name = request.json.get("last_name", None),
        account_type = request.json.get("account_type", None),
        theme_type = 'light'
    )
    API.save_changes(newAcc)
    return jsonify(
        status='saved',
    ), 200


@app.route("/fetch/<uid>", methods=["GET"])
@jwt_required()
def fetch(uid):
    accDetails = AccountDetails.query.filter_by(user_id=uid).first()
    return jsonify(
        status='saved',
        data=accDetails.serialize(),
    ), 200


@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    claims = get_jwt()

    if "pro_img" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["pro_img"]

    if file.filename == "":
        return "Please select a file"


    if file and file.mimetype == 'image/jpeg':
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"], claims['id'])
        return jsonify(
            img_url=str(output),
        ), 200

    else:
        return jsonify(
            msg='Invalid File',
        ), 200

