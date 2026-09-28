from datetime import datetime, date
from . import db


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lesson = db.relationship('Lesson', lazy='joined')

    def __repr__(self):
        return f'<UserProgress User:{self.user_id} Lesson:{self.lesson_id} Completed:{self.is_completed}>'


class VocabularyProgress(db.Model):
    __tablename__ = 'vocabulary_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'), nullable=False)
    is_mastered = db.Column(db.Boolean, default=False, nullable=False)
    last_reviewed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vocabulary = db.relationship('Vocabulary', lazy='joined')

    def __repr__(self):
        return f'<VocabularyProgress User:{self.user_id} Vocab:{self.vocabulary_id} Mastered:{self.is_mastered}>'


class UserStreak(db.Model):
    __tablename__ = 'user_streaks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_date = db.Column(db.Date, default=date.today, nullable=False)
    xp_earned = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<UserStreak User:{self.user_id} Date:{self.activity_date} XP:{self.xp_earned}>'