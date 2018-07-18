from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flashlearn.auth import login_required
from flashlearn.db import get_db

bp = Blueprint('flashcard', __name__)

@bp.route('/flashcard/')
def index():
#     return 'hi'
    db = get_db()
    flashcards = db.execute(
        'SELECT id, question, answer'
        ' FROM flashcard'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('flashcard/index.html', flashcards=flashcards)

