from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin



db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='user', lazy='dynamic', cascade="all, delete-orphan")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic', cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Post "{self.title}">'

    @property
    def like_count(self):
        # Efficiently count likes without loading them
        return db.session.query(Like.id).filter_by(post_id=self.id).count()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates="comments")
    post = db.relationship('Post', back_populates="comments")

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Like by user_id {self.user_id} on post_id {self.post_id}>'
