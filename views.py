import json

from flask import Blueprint, request, flash, jsonify
from flask import render_template
from flask_login import current_user, login_required
from models import Note, db

views = Blueprint('views', __name__)


@views.route('/',methods=['GET','POST'])
@login_required
def home_page():
    if request.method == 'POST':
        data = request.form.get('note')
        if len(data) < 1:
            flash('Note is too short!', category='error')
        else:
            user = current_user
            note = Note(data=data, user_id=user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note Added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})