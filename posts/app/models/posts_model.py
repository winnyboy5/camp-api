from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Comment(db.Model):
    __tablename__ = 'camp_comments'
    coid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('camp_posts.pid'))
    card_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.post_id}, {self.card_id}, '{self.content}', '{self.created_at}')"


class Likes(db.Model):
    __tablename__ = 'camp_likes'
    lid = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('camp_posts.pid'))
    card_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.post_id}, {self.card_id}, '{self.created_at}')"


class Media(db.Model):
    __tablename__ = 'camp_post_media'
    lid = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('camp_posts.pid'))
    post_type = db.Column(db.String(50), nullable=False)
    media_link = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.post_id}, {self.card_id}, '{self.created_at}')"

class Post(db.Model):
    __tablename__ = 'camp_posts'
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    media_id = db.relationship('Media')
    card_id = db.Column(db.Integer, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)

    likes = db.relationship('Likes')
    comments = db.relationship('Comment')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.content}', '{self.created_at}')"





