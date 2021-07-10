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

from app.models.posts_model import Post


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


@app.route("/post", methods=["POST"])
@jwt_required()
def upload_file():
    try:
        # Access the identity of the current user with get_jwt_identity
        claims = get_jwt()
        print(request)

        if "post_img" in request.files:
            file = request.files["post_img"]
            if file.filename == "":
                return "Please select a file"

        img_sizes = [(1080,1080)]

        print(file)

        uploadId = str(uuid.uuid4().hex)

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


        print(request.form)
        
        newPost = Post(
            user_id = claims['id'],
            content = request.form["content"],
            card_id = request.form["card_id"],
            media_id = uploadId,
            post_type = request.form["post_type"]
        )
        API.save_changes(newPost)

    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    
    return jsonify(
        msg="success",
    ), 200 


@app.route("/post/<int:post_id>/like/<int:card_id>", methods=['GET', 'POST'])
@jwt_required()
def post_likes(post_id,card_id):
    post = Post.query.get(int(post_id))

    post.like_post(card_id)
    API.save_changes(post)
        
    return jsonify(likes=post.get_likes_count()), 200


@app.route("/post/comment", methods=['POST'])
@jwt_required()
def post_comment():
    post = Post.query.get(int(request.json.get("post_id", None)))

    post.add_comment(request.json.get("card_id", None),request.json.get("comment", None))

    API.save_changes(post)
        
    return jsonify(
        msg="success",
    ), 200
    
@app.route("/post/comment/delete", methods=['POST'])
@jwt_required()
def post_comment_delete():
    post = Post.query.get(int(request.json.get("post_id", None)))

    post.remove_comment(request.json.get("coid", None))
    API.save_changes(post)

    return jsonify(
        msg="success",
    ), 200 