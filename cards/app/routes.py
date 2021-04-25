import os
from app import app
from app.api import API
from flask import request, jsonify

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt

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
        username=claims['username'],
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
    # Access the identity of the current user with get_jwt_identity
    claims = get_jwt()
    newCard = Card(
        user_id = claims['id'],
        email = request.json.get("email", None)
        phone = request.json.get("phone", None)
        website = request.json.get("website", None)
        user_card = request.json.get("user_card", None)
        role = request.json.get("role", None)
        organization = request.json.get("organization", None)
        user_image = request.json.get("user_image", None)
        brand_image = request.json.get("brand_image", None)
        card_type = request.json.get("card_type", None)
        primary_color = request.json.get("primary_color", None)
        text_color = request.json.get("text_color", None)
    )
    API.save_changes(newCard)
    return jsonify(
        status='saved',
    ), 200


@app.route("/fetchcards", methods=["GET"])
@jwt_required()
def fetch_cards(uid):
    cards = Card.query.all()
    return jsonify(
        status='saved',
        data=[card.serialize() for card in cards],
    ), 200