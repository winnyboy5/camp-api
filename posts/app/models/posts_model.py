from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.api import API



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
        return f"Liked({self.post_id}, {self.card_id}, '{self.created_at}')"


# class Notif(db.Model):
#     __tablename__ = 'camp_notifs'
#     nid = db.Column(db.Integer, primary_key=True)
#     msg = db.Column(db.Text, nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.pid'), nullable=False)
#     for_uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
#     author = db.Column(db.String(20), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


#     @staticmethod
#     def add_notif(user, post, n_type):
#         notif_for = post.author.uid
#         n = Notif(for_uid=notif_for, post_id=post.pid, msg=n_type, author=user.username)
#         return n

#     def __repr__(self):
#         return f"{self.author} {self.msg} your post({self.post_id})"


class Post(db.Model):
    __tablename__ = 'camp_posts'
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_id = db.Column(db.String(200), nullable=False)
    card_id = db.Column(db.Integer, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)

    likes = db.relationship('Likes', backref='camp_posts', lazy='dynamic')
    comments = db.relationship('Comment', backref='camp_posts', lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_likes_count(self):
        return Likes.query.filter_by(post_id=self.pid).count()

    def like_post(self, card_id):
        if Likes.query.filter_by(post_id=self.pid,card_id=int(card_id)).first() is None:
            l = Likes(post_id=self.pid,card_id=card_id)            
            self.likes.append(l)
            return "like"
        else:
            self.unlike_post(card_id)
            return "unlike"

    def unlike_post(self, card_id):
        u = Likes.query.filter_by(post_id=self.pid,card_id=int(card_id)).delete()

    def add_comment(self, card_id, comment):
        c = Comment(post_id=self.pid,card_id=card_id,content=comment)
        self.comments.append(c)
        return True

    def remove_comment(self, coid):
        print(coid)
        rc = Comment.query.filter_by(coid=int(coid)).delete()
        return True



    def __repr__(self):
        return f"Post('{self.content}', '{self.created_at}')"





