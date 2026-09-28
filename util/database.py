from model import db, Language, Course, Unit, Lesson, Question, Option, Vocabulary
from sqlalchemy.exc import SQLAlchemyError

def init_db(app):
    """
    Initializes the database by creating all tables defined in SQLAlchemy models.
    """
    with app.app_context():
        db.create_all()


def seed_default_data():
    """
    Seeds the database with initial languages, sample courses, and units
    if the database is currently empty.
    """
    try:
        if Language.query.first() is not None:
            return False  # Database already seeded

        # 1. Add Default Languages
        spanish = Language(
            name='Spanish',
            code='es',
            flag='🇪🇸',
            level='Beginner to Advanced (A1 - C1)',
            region='Spain & Latin America',
            description='Master conversational Spanish through immersive daily practice.'
        )
        french = Language(
            name='French',
            code='fr',
            flag='🇫🇷',
            level='Beginner to Intermediate (A1 - B2)',
            region='France & Canada',
            description='Learn essential French phrases, grammar, and pronunciation.'
        )
        german = Language(
            name='German',
            code='de',
            flag='🇩🇪',
            level='Beginner to Intermediate (A1 - B2)',
            region='Germany & Central Europe',
            description='Build a solid foundation in German vocabulary and sentence structure.'
        )

        db.session.add_all([spanish, french, german])
        db.session.flush()

        # 2. Add Sample Spanish Course & Unit
        es_course = Course(
            title='Spanish Foundations',
            description='Start your journey learning conversational Spanish.',
            language_id=spanish.id
        )
        db.session.add(es_course)
        db.session.flush()

        es_unit = Unit(
            title='Unit 1: Basic Greetings & Introductions',
            description='Learn how to greet people and introduce yourself.',
            order_number=1,
            course_id=es_course.id
        )
        db.session.add(es_unit)
        db.session.flush()

        # 3. Add Sample Lesson
        es_lesson = Lesson(
            title='Common Greetings',
            description='Basic hello, goodbye, and polite phrases.',
            order_number=1,
            xp_reward=20,
            estimated_minutes=5,
            unit_id=es_unit.id
        )
        db.session.add(es_lesson)
        db.session.flush()

        # 4. Add Sample Question & Options
        q1 = Question(
            prompt='How do you say "Good morning" in Spanish?',
            target_text='¡Buenos días!',
            lang_code='es-ES',
            explanation='"¡Buenos días!" is used until noon to say good morning.',
            lesson_id=es_lesson.id
        )
        db.session.add(q1)
        db.session.flush()

        opt1 = Option(text='¡Buenos días!', is_correct=True, question_id=q1.id)
        opt2 = Option(text='Buenas noches', is_correct=False, question_id=q1.id)
        opt3 = Option(text='Hasta luego', is_correct=False, question_id=q1.id)
        db.session.add_all([opt1, opt2, opt3])

        # 5. Add Sample Vocabulary
        vocab1 = Vocabulary(
            term='¡Buenos días!',
            phonetic='[bwe-nos dee-as]',
            translation='Good morning!',
            category='Greetings',
            pos='phrase',
            example='¡Buenos días! ¿Cómo estás?',
            lang_code='es-ES',
            lesson_id=es_lesson.id
        )
        db.session.add(vocab1)

        db.session.commit()
        return True

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")
        return False


def commit_or_rollback():
    """
    Helper function to safely commit database changes or rollback if an error occurs.
    """
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during commit: {e}")
        return False


def reset_db(app):
    """
    Drops all existing database tables and recreates them.
    (Useful for testing or resetting development data).
    """
    with app.app_context():
        db.drop_all()
        db.create_all()