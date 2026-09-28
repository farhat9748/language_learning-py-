from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Gamification & Learning Metrics
    streak = db.Column(db.Integer, default=0, nullable=False)
    lives = db.Column(db.Integer, default=5, nullable=False)
    total_xp = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Active Workspace Foreign Key
    target_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=True)

    # Database Relationships
    target_language = db.relationship('Language', foreign_keys=[target_language_id], lazy='joined')
    progress_records = db.relationship('UserProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    streak_records = db.relationship('UserStreak', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    # Password Management Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Helper Utilities
    def reset_lives(self, count=5):
        self.lives = count

    def add_xp(self, amount):
        self.total_xp += amount

    def __repr__(self):
        return f'<User {self.username}>'