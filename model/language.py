from . import db

class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., 'es', 'fr', 'de'
    flag = db.Column(db.String(10), nullable=False, default='🌐')
    level = db.Column(db.String(64), default='Beginner to Advanced (A1 - C1)', nullable=False)
    region = db.Column(db.String(64), default='Global', nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Database Relationships
    courses = db.relationship('Course', backref='language', lazy='select', cascade='all, delete-orphan')

    @property
    def total_lessons(self):
        return sum(len(unit.lessons) for course in self.courses for unit in course.units)

    @property
    def vocab_count(self):
        return sum(
            len(lesson.vocabulary) 
            for course in self.courses 
            for unit in course.units 
            for lesson in unit.lessons
        )

    @property
    def active_learners_count(self):
        from .user import User
        return User.query.filter_by(target_language_id=self.id).count()

    def __repr__(self):
        return f'<Language {self.name} ({self.code})>'