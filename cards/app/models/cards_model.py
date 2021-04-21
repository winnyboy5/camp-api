from app import db
from datetime import datetime


class AccountDetails(db.Model):
    __tablename__ = 'camp_cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    is_verified = db.Column(db.Boolean,default=False, nullable=False)
    account_type = db.Column(db.String(120), nullable=False)
    profile_image_id = db.Column(db.String(120), nullable=False)
    theme_type = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<AccountDetails %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "mobile": self.mobile,
            "country": self.country,
            "created_at": self.created_at.isoformat()+"Z",
            "updated_at": self.updated_at.isoformat()+"Z" }

