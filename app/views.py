
from flask import Blueprint, render_template,redirect, url_for, request
from flask_login import login_required, logout_user, current_user
from .models import Note
from . import db

app = Blueprint('views',__name__)

@app.route('/')
@app.route('/notes')
@login_required
def home():
    return render_template('content/partials/home.html') if request.headers.get('HX-Request') else render_template('content/home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@app.route('/new-note', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form.get('note-title')
        about = request.form.get('note-about')
        new_note = Note(title=title, about=about, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return render_template('content/partials/note.html', note=new_note)
    return render_template('content/new_note.html')

@app.route('/delete-note/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    note.user_id = current_user.id
    db.session.delete(note)
    db.session.commit()
    return ""

@app.route('/about/<int:id>')
def about_note(id):
    note = Note.query.get_or_404(id)
    if request.headers.get('HX-Request', '').lower() == 'true':
        return render_template('content/partials/about_note.html', note=note)
    else:
        return render_template('content/about_note.html', note=note)
    
@app.route('/search')
def search_notes():
    search_term = request.args.get('q', '')
    user_id = current_user.id  # Assuming you're using Flask-Login
    
    query = Note.query.filter_by(user_id=user_id)
    
    if search_term:
        query = query.filter(
            (Note.title.ilike(f'%{search_term}%')) | 
            (Note.about.ilike(f'%{search_term}%'))
        )
    notes = query.all()
    return render_template('content/partials/search_notes.html', notes=notes)

@app.route('/edit-note/<int:id>', methods=['PUT','GET'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'PUT':
        note.title = request.form.get('note-title')
        note.about = request.form.get('note-about')
        note.user_id = current_user.id
        db.session.commit()
        return render_template('content/partials/about_note.html', note=note)
    return render_template('content/partials/edit_note.html', note=note)