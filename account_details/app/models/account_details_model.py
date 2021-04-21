from app import db
from datetime import datetime


class AccountDetails(db.Model):
    __tablename__ = 'camp_account_details'
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
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_verified": self.is_verified,
            "account_type": self.account_type,
            "profile_image_id": self.profile_image_id,
            "theme_type": self.theme_type,
            "created_at": self.created_at.isoformat()+"Z",
            "updated_at": self.updated_at.isoformat()+"Z" }

