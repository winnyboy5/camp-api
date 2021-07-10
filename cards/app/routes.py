import os
from app import app
from app.api import API
from flask import request, jsonify

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt 

from utils.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from PIL import Image
import io
import uuid

from app.models.cards_model import Card


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
        # Access the identity of the current user with get_jwt_identity
        claims = get_jwt()
        if request.json.get("base_card", None):
            cardCheck = Card.query.filter_by(user_id=claims['id'], base_card=True).first()
            print(cardCheck)
            if cardCheck:
                return jsonify(
                status='DENIED',
            ), 200
        
        newCard = Card(
            user_id = claims['id'],
            email = request.json.get("email", None),
            phone = request.json.get("phone", None),
            website = request.json.get("website", None),
            base_card = request.json.get("base_card", None),
            role = request.json.get("role", None),
            organization = request.json.get("organization", None),
            org_type = request.json.get("org_type", None),
            card_type = request.json.get("card_type", None),
            primary_color = request.json.get("primary_color", None),
            text_color = request.json.get("text_color", None)
        )
        API.save_changes(newCard)

    except Exception as e:
        print("Something Happened: ", e)
        return e
        
    return jsonify(
        status='saved',
    ), 200


@app.route("/fetchcards", methods=["GET"])
@jwt_required()
def fetch_cards():
    cards = Card.query.all()
    return jsonify(
        status='saved',
        data=[card.serialize() for card in cards],
    ), 200


@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    claims = get_jwt()
    print(request)
    cardUpdate = Card.query.filter_by(id=request.form.get('card_id')).first()

    if "brand_img" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["brand_img"]

    if file.filename == "":
        return "Please select a file"

    img_sizes = [(128,128),(256,256)]
    
    if cardUpdate.brand_image is None:
        uploadId = str(uuid.uuid4().hex)
    else:
        uploadId = cardUpdate.brand_image

    print(file)

    if file and (file.mimetype == 'image/jpeg' or file.mimetype == 'image/png'):
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
        
            cardUpdate.brand_image = uploadId
            API.save_changes(cardUpdate)

        return jsonify(
            msg="success",
        ), 200 

