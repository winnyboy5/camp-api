from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Card(db.Model):
    __tablename__ = 'camp_cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(80))
    website = db.Column(db.String(120))
    user_card = db.Column(db.Boolean,default=False, nullable=False)
    role = db.Column(db.String(120), nullable=False)
    organization = db.Column(db.String(120))
    user_image = db.Column(db.String(120), nullable=False)
    brand_image = db.Column(db.String(120), nullable=False)
    card_type = db.Column(db.String(120), nullable=False)
    primary_color = db.Column(db.String(20), nullable=False)
    text_color = db.Column(db.String(20), nullable=False)
    review = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<card %r>' % self.cid

    def serialize(self):
        return {
            "cid": self.cid,
            "user_id": self.user_id,
            "email": self.email,
            "phone": self.phone,
            "user_card": self.user_id,
            "role": self.role,
            "user_image": self.user_image,
            "brand_image": self.brand_image,
            "card_type": self.card_type,
            "primary_color": self.primary_color,
            "text_color": self.text_color,
            "created_at": self.created_at.isoformat()+"Z",
            "updated_at": self.updated_at.isoformat()+"Z" }

