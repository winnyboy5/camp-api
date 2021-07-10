import os
from app import app
from app.api import API
from flask import request, jsonify
from utils.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from PIL import Image
import io
import uuid


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
    try:
        claims = get_jwt()
        newAcc = AccountDetails(
            user_id = claims['id'],
            first_name = request.json.get("first_name", None),
            last_name = request.json.get("last_name", None),
            account_type = request.json.get("account_type", None),
            theme_type = 'l'
        )
        API.save_changes(newAcc)
        return jsonify(
            status='saved',
        ), 200
    
    except Exception as e:
        print("Something Happened: ", e)
        return e


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
    accUpdate = AccountDetails.query.filter_by(user_id=claims['id']).first()

    if "pro_img" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["pro_img"]

    if file.filename == "":
        return "Please select a file"

    img_sizes = [(128,128),(256,256)]
    
    if accUpdate.profile_image_id is None:
        uploadId = str(uuid.uuid4().hex)
    else:
        uploadId = accUpdate.profile_image_id

    print(file)

    if file and file.mimetype == 'image/jpeg':
        for size in img_sizes:
            image = Image.open(file).convert("RGBA")
            image_io = io.BytesIO()
            image.thumbnail(size, Image.ANTIALIAS)
            if image.format == "RGB":
                image.save(image_io, "JPEG", optimize=True) 
            else:
                result  = Image.new('RGB', (image.width,image.height), color=(255,255,255))
                result.paste(image,image)
                result.save(image_io, "JPEG", optimize=True)
                
            thumbName = '%s_%s.jpg' % (uploadId, str('x'.join(tuple(map( str , size )))))
            image_io.seek(0)
            output = upload_file_to_s3(image_io, app.config["S3_BUCKET"], claims['user_name'], thumbName, file.content_type)        
        
            accUpdate.profile_image_id = uploadId
            API.save_changes(accUpdate)

        return jsonify(
            msg="success",
        ), 200   

    # if file and file.mimetype == 'image/jpeg':
    #     file.filename = secure_filename(file.filename)
    #     output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"], claims['user_name'])
    #     return jsonify(
    #         img_url=str(output),
    #     ), 200

    # else:
    #     return jsonify(
    #         msg='Invalid File',
    #     ), 200

