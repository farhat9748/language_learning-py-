from flask import Blueprint, render_template

from model import Language

language_bp = Blueprint('language', __name__)

@language_bp.route('/languages')
def list_languages():
    languages = Language.query.all()
    return render_template('language/language.html', languages=languages)

@language_bp.route('/language/<int:language_id>')
def language_detail(language_id):
    language = Language.query.get_or_404(language_id)
    return render_template('language/language_detail.html', language=language)