from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .language import Language
from .course import Course, Unit, Lesson, Question, Option
from .progress import UserProgress, VocabularyProgress, UserStreak

__all__ = ['db', 'User', 'Language', 'Course', 'Unit', 'Lesson', 'Question', 'Option', 'UserProgress', 'VocabularyProgress', 'UserStreak']